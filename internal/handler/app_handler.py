#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/29 14:59
@Author  : thezehui@gmail.com
@File    : app_handler.py
"""

# venv/bin/python -m app.http.app
import uuid
from dataclasses import dataclass
from uuid import UUID

from flask import Response, stream_with_context
from injector import inject
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableParallel

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经成功创建，id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是:{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id为:{app.id}")

    def debug(self, app_id: UUID):
        """聊天接口"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.构建组件
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个乐于助人的AI助手，请始终使用中文回答用户的问题。"),
            ("human", "{query}"),
        ])
        
        llm = ChatOllama(base_url="http://127.0.0.1:11434", model="llama3")
        parser = StrOutputParser()

        # 3.构建链
        chain = prompt | llm | parser

        # 4.直接去请求ollama服务
        response = chain.invoke({"query": req.query})
       
        # 5.返回结果
        return success_json(response)

    def ping(self):
        raise FailException("数据未找到")


    def test(self):
        
        
        llm = ChatOllama(base_url="http://127.0.0.1:11434", model="llama3")
        # llm = ChatKimi(
        #     api_key="sk-WV9gIziS8Cp3PtuvjHZAKHehLqAm17aafaRRlfI64RS97asi",
        #     model="kimi-llm-4k"
        # )
        
        parser = StrOutputParser()
        # 2.构建一个提示模板
        prompt = ChatPromptTemplate.from_messages([
                ("system", "请始终使用中文汉字回答用户的问题。"),
                ("human", "请根据用户的提问进行回答，必须使用中文。\n{query}")
            ])

        joke_prompt = ChatPromptTemplate.from_template("请讲一个关于{subject}的冷笑话，尽可能短一些")
        poem_prompt = ChatPromptTemplate.from_template("请写一篇关于{subject}的诗，尽可能短一些")
        
        joke_chain = joke_prompt | llm | parser
        poem_chain = poem_prompt | llm | parser
        
        map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)
        map_chain_response = map_chain.invoke({"subject": "程序员"})
        
        return success_json(map_chain_response)
        
      

       
