import unittest
from scripts.load_data import SYSTEM_PROMPT, training_messages


class LoaderTests(unittest.TestCase):
    def test_structured_case(self):
        row = {"instruction": "任务", "question": "问题", "answer": "回答", "context_documents": [{"id": "law:1", "title": "法源", "source_url": "https://example.org/law", "content": "原文"}]}
        result = training_messages(row)
        self.assertEqual(result[0]["content"], SYSTEM_PROMPT)
        self.assertEqual(result[-1], {"role": "assistant", "content": "回答"})
        self.assertIn("[law:1] 法源\n来源：https://example.org/law\n原文", result[1]["content"])

    def test_multiturn(self):
        result = training_messages({"messages": [{"role": "user", "content": "一"}, {"role": "assistant", "content": "二"}, {"role": "user", "content": "三"}, {"role": "assistant", "content": "四"}]})
        self.assertEqual([r["role"] for r in result], ["system", "user", "assistant", "user", "assistant"])
        self.assertEqual(result[-1]["content"], "四")
        self.assertIn("【参考资料】", result[3]["content"])

    def test_bad_roles(self):
        with self.assertRaises(ValueError):
            training_messages({"messages": [{"role": "assistant", "content": "bad"}]})


if __name__ == "__main__":
    unittest.main()
