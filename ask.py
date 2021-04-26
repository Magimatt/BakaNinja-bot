import os
from dotenv import load_dotenv
import wolframalpha
import asyncio
import requests


class Ask:
    ###############
    # CONSTRUCTOR #
    ###############
    def __init__(self, prefix, ctx=None):
        self.__PREFIX = prefix
        self.__CTX = ctx

        load_dotenv()
        self.__TOKEN = os.getenv("WOLFRAM_ALPHA_TOKEN")
        self.__wolf = wolframalpha.Client(self.__TOKEN)

    #####################
    # GETTERS & SETTERS #
    #####################
    def get_CTX(self):
        return self.__CTX

    def set_CTX(self, ctx):
        self.__CTX = ctx

    #################
    # CLASS METHODS #
    #################
    # def __build_api_request(self, query):
    #     url = f"https://api.wolframalpha.com/v1/result?i={query}&appid={__TOKEN}"

    #     response = ''
    #     return response

    # Think about using the "short-answers-api" version for this feature in the future
    async def return_response_ask(self, arg=None):
        response = ''
        if arg is None:
            response = ("This command requires an argument.\n"
                        "Try asking me a question about math, science, history, music, or whatever. Magimatt-san made me sooo smart!\n"
                        'For example type: "~question What was the weather like on April 24th 2021 in Prescott Valley, AZ"')
        else:
            query_result = self.__wolf.query(arg)

            # print(f"Success: {query_result['@success']}")  # debug
            # print(f"error: {query_result['@error']}")  # debug
            print(query_result)  # debug

            # # First iteration of getting the plain text answer
            # response = next(query_result.results).text
            
            # Alternate method of printing the plaintext from the pods
            for pod in query_result.pods:
                # finds all plaintext in the subpods and concat to response
                for subpod in pod.subpods:
                    if not subpod.plaintext is None:
                        response = response + subpod.plaintext + '\n'
            
            if (query_result['@success'] == False
                or query_result['@error'] == True
                or response == ''):
                response = ("Huh...? I'm not sure I understood you right.\n"
                            "Would you try rephrasing the question and asking me again.\n"
                            "Unless...*GASP*...I don't know the answer! Please forgive me senpai!")

            try:
                response = subpod['imagesource']
            except:
                pass
        return response

        # TODO: implement wolfram alpha API's <didyoumean> pod to recommend a search string.
        # https://products.wolframalpha.com/api/documentation/#queries-that-are-not-understood

    def return_response_trivia(self):
        pass
