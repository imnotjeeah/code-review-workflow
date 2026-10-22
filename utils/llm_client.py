import os
import time
from openai import OpenAI


class LLMClient:
    def __init__(self, max_retries: int = 3):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
        self.max_retries = max_retries

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self.client.chat.completions.create(
                    model=os.getenv("MODEL", "gpt-4o-mini"),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                return resp.choices[0].message.content
            except Exception as e:
                last_error = e
                print(f"[LLMClient] 第 {attempt} 次调用失败: {e}")
                time.sleep(1)

        raise RuntimeError(f"LLM 调用失败，已重试 {self.max_retries} 次: {last_error}")