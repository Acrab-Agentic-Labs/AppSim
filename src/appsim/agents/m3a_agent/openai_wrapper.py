# -*- coding: utf-8 -*-
"""OpenAI LLM Wrapper for M3A Agent"""

import base64
import logging
import time
from typing import Optional, Any
import numpy as np
from PIL import Image
import io
from openai import OpenAI


def array_to_jpeg_bytes(image: np.ndarray) -> bytes:
    """Converts a numpy array into a byte string for a JPEG image."""
    image = Image.fromarray(image)
    return image_to_jpeg_bytes(image)


def image_to_jpeg_bytes(image: Image.Image) -> bytes:
    """Converts a PIL Image into JPEG bytes."""
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format="JPEG")
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()
    return img_bytes


class OpenAIWrapper:
    """OpenAI Multimodal LLM Wrapper for M3A Agent.

    使用 OpenAI API 的 chat.completions.create 方法实现多模态 LLM 调用。
    """

    ERROR_CALLING_LLM = "Error calling LLM"
    RETRY_WAITING_SECONDS = 20

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
        max_retry: int = 3,
        model_kwargs: Optional[dict] = None,
    ):
        """初始化 OpenAI Wrapper.

        Args:
            api_key: OpenAI API密钥（必需位置参数）
            base_url: OpenAI API基础URL（必需位置参数）
            model_name: OpenAI 模型名称（必需位置参数），如 'gpt-4o', 'gpt-4-turbo' 等
            max_retry: 最大重试次数（可选关键字参数）
            model_kwargs: 传递给 chat.completions.create 的额外关键字参数（可选关键字参数）
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name
        self.model_kwargs = model_kwargs or {}

        if max_retry <= 0:
            max_retry = 3
            logging.warning("Max_retry must be positive. Reset it to 3")
        self.max_retry = min(max_retry, 5)

    @classmethod
    def encode_image(cls, image: np.ndarray) -> str:
        """将 numpy 数组编码为 base64 字符串."""
        return base64.b64encode(array_to_jpeg_bytes(image)).decode("utf-8")

    def predict_mm(self, text_prompt: str, images: list[np.ndarray]) -> tuple[str, Optional[bool], Any]:
        """调用多模态 LLM.

        Args:
            text_prompt: 文本提示
            images: 图像列表（numpy 数组）

        Returns:
            tuple: (输出文本, is_safe, 原始响应)
        """
        # 构建消息内容
        content = [{"type": "text", "text": text_prompt}]

        # 添加图像
        for image in images:
            base64_image = self.encode_image(image)
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})

        counter = self.max_retry
        wait_seconds = self.RETRY_WAITING_SECONDS

        while counter > 0:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name, messages=[{"role": "user", "content": content}], **self.model_kwargs
                )

                if response.choices and len(response.choices) > 0:
                    text_output = response.choices[0].message.content
                    return text_output, None, response
                else:
                    logging.error("Error: No choices in response")
                    time.sleep(wait_seconds)
                    wait_seconds *= 2

            except Exception:
                logging.error(f"Error calling LLM, will retry in {wait_seconds} seconds")
                time.sleep(wait_seconds)
                wait_seconds *= 2
                counter -= 1

        return self.ERROR_CALLING_LLM, None, None
