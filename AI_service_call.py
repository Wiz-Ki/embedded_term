from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional
from typing import Dict, Any
from prompts import PROMPT_TEMPLATE
import os

class IoTResponse(BaseModel):
    action: str = Field(..., description="The specific action to be taken (turn_on, turn_off, set_temperature, set_brightness, set_channel, set_volume, set_mode)")
    device: str = Field(..., description="The target device (lights, heater, airconditioner, tv)")
    value: Optional[int] = Field(None, description="Optional numerical value or mode setting (if applicable)")
    status: str = Field(..., description="The status of the action (success/failed)")
    response: str = Field(..., description="Natural Korean response")

class AISpeakerCall:

    def __init__(self):
        #load dotenv
        load_dotenv()

        #Set Langchain
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=os.getenv("MODEL_NAME", "gpt-4o-mini"),
            temperature=1.3,
        )

        # 출력 스키마 설정 (모델의 출력 형태 설정)
        self.response_schemas = [
            ResponseSchema(name="action", description="The specific action to be taken (turn_on, turn_off, set_temperature, set_brightness, set_channel, set_volume, set_mode)"),
            ResponseSchema(name="device", description="The target device (lights, heater, airconditioner, tv)"),
            ResponseSchema(name="value", description="(optional) Optional numerical value or mode setting (if applicable)"),
            ResponseSchema(name="status", description="The status of the action (success/failed)"),
            ResponseSchema(name="response", description="Natural Korean response"),

        ]

        # Create output parser
        self.output_parser = PydanticOutputParser(pydantic_object=IoTResponse)
        # 포맷 지침 가져오기
        self.format_instructions = self.output_parser.get_format_instructions()

        # 프롬프트 템플릿 정의
        template = PROMPT_TEMPLATE

        self.prompt = ChatPromptTemplate.from_template(template)

    def process_conversation(self, user_input, conversation_history=""):
        try:
            # 체인 생성 및 실행
            chain = self.prompt | self.llm
            result = chain.invoke({
                "format_instructions": self.format_instructions,
                "user_input": user_input,
                "conversation_history": conversation_history,
            })

            # 결과 파싱(JSON형태 리턴 -> Python Dict형태)
            parsed_output = self.output_parser.parse(result.content)

            response = parsed_output.model_dump()

            return response

        except Exception as e:
            return {
                "action": "error",
                "device": "none",
                "status": "failed",
                "response": f"죄송합니다. 처리 중 오류가 발생했습니다: {str(e)}"
            }


if __name__ == "__main__":
    # 테스트 코드
    iot_speaker = AISpeakerCall()

    # 테스트할 사용자 입력 목록
    test_inputs = [
        "에어컨을 24도로 설정해 주세요.",
        "조명을 켜줘.",
        "TV를 10번 채널로 바꿔줘.",
        "히터 온도를 35도로 맞춰줘.",  # 온도 범위 초과 (에러 처리 확인)
        "불을 꺼줘.",
        "에어컨을 냉방 모드로 전환해줘.",
        "볼륨을 50으로 올려줘.",
        "에어컨 온도를 17도로 낮춰줘.",  # 에어컨 온도 범위의 최저값 확인
        "에어컨을 15도로 설정해줘.",  # 에어컨 온도 범위 이하 (에러 처리 확인)
        "TV를 켜고 7번 채널로 맞춰줘.",
        "조명 밝기를 120으로 설정해줘.",  # 밝기 범위 초과 (에러 처리 확인)
    ]

    for user_input in test_inputs:
        response = iot_speaker.process_conversation(user_input)
        print(f"사용자 입력: {user_input}")
        print("응답:", response)
        print("-" * 50)
