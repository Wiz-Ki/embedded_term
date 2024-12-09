import unittest
from unittest.mock import patch, Mock
import json
from AI_service_call import AISpeakerCall


class TestAISpeakerCall(unittest.TestCase):
    def setUp(self):
        self.speaker = AISpeakerCall()

    def test_basic_device_control(self):
        """기본적인 기기 제어 테스트"""
        mock_content = """
        {
            "action": "turn_off",
            "device": "lights",
            "status": "success",
            "response": "네, 조명을 끄도록 하겠습니다."
        }
        """

        # ChatPromptTemplate과 LLM 모두 모킹
        with patch('langchain.prompts.ChatPromptTemplate.from_template') as mock_template, \
                patch('langchain_openai.ChatOpenAI') as mock_llm:
            mock_chain = Mock()
            mock_chain.invoke.return_value = Mock(content=mock_content)
            self.speaker.llm = mock_llm
            self.speaker.prompt = mock_template
            mock_template.__or__.return_value = mock_chain

            result = self.speaker.process_conversation("조명 꺼줘")

            self.assertEqual(result["action"], "turn_off")
            self.assertEqual(result["device"], "lights")
            self.assertEqual(result["status"], "success")

    def test_temperature_control(self):
        """온도 조절 명령 테스트"""
        mock_content = """
        {
            "action": "set_temperature",
            "device": "airconditioner",
            "value": 24,
            "status": "success",
            "response": "에어컨 온도를 24도로 설정했습니다."
        }
        """

        with patch('langchain.prompts.ChatPromptTemplate.from_template') as mock_template, \
                patch('langchain_openai.ChatOpenAI') as mock_llm:
            mock_chain = Mock()
            mock_chain.invoke.return_value = Mock(content=mock_content)
            self.speaker.llm = mock_llm
            self.speaker.prompt = mock_template
            mock_template.__or__.return_value = mock_chain

            result = self.speaker.process_conversation("에어컨 온도 24도로 설정해줘")

            self.assertEqual(result["action"], "set_temperature")
            self.assertEqual(result["device"], "airconditioner")
            self.assertEqual(result["value"], 24)

    def test_error_handling(self):
        """에러 처리 테스트"""
        with patch('langchain.prompts.ChatPromptTemplate.from_template') as mock_template:
            mock_chain = Mock()
            mock_chain.invoke.side_effect = Exception("테스트 에러")
            self.speaker.prompt = mock_template
            mock_template.__or__.return_value = mock_chain

            result = self.speaker.process_conversation("잘못된 명령")

            self.assertEqual(result["action"], "error")
            self.assertEqual(result["status"], "failed")
            self.assertTrue("오류가 발생했습니다" in result["response"])

    def test_invalid_temperature(self):
        """잘못된 온도값 테스트"""
        mock_content = """
        {
            "action": "set_temperature",
            "device": "heater",
            "status": "failed",
            "response": "설정 가능한 온도는 16-30도 사이입니다."
        }
        """

        with patch('langchain.prompts.ChatPromptTemplate.from_template') as mock_template, \
                patch('langchain_openai.ChatOpenAI') as mock_llm:
            mock_chain = Mock()
            mock_chain.invoke.return_value = Mock(content=mock_content)
            self.speaker.llm = mock_llm
            self.speaker.prompt = mock_template
            mock_template.__or__.return_value = mock_chain

            result = self.speaker.process_conversation("히터 온도 35도로 설정해줘")

            self.assertEqual(result["status"], "failed")
            self.assertTrue("16-30도" in result["response"])

    def test_conversation_history(self):
        """대화 기록 처리 테스트"""
        mock_content = """
        {
            "action": "set_temperature",
            "device": "airconditioner",
            "value": 24,
            "status": "success",
            "response": "에어컨 온도를 24도로 설정했습니다."
        }
        """

        with patch('langchain.prompts.ChatPromptTemplate.from_template') as mock_template, \
                patch('langchain_openai.ChatOpenAI') as mock_llm:
            mock_chain = Mock()
            mock_chain.invoke.return_value = Mock(content=mock_content)
            self.speaker.llm = mock_llm
            self.speaker.prompt = mock_template
            mock_template.__or__.return_value = mock_chain

            result = self.speaker.process_conversation(
                "온도 24도로 설정해줘",
                conversation_history="사용자: 에어컨 켜줘\nAI: 네, 에어컨을 켰습니다."
            )

            self.assertEqual(result["action"], "set_temperature")
            self.assertEqual(result["device"], "airconditioner")


if __name__ == '__main__':
    unittest.main()