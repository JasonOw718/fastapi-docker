from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
import base64
import os
from langchain_core.messages import HumanMessage
import time
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings,GoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def encode_image(image_path):
    """Getting the base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def image_summarize(img_base64, prompt):
    """Make image summary"""
    try:
      chat = ChatGoogleGenerativeAI(model="gemini-1.0-pro-001",temperature=0)

      msg = chat.invoke(
          [
              HumanMessage(
                  content=[
                      {"type": "text", "text": prompt},
                      {
                          "type": "image_url",
                          "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                      },
                  ]
              )
          ]
      )
    except:
      chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0)

      msg = chat.invoke(
          [
              HumanMessage(
                  content=[
                      {"type": "text", "text": prompt},
                      {
                          "type": "image_url",
                          "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                      },
                  ]
              )
          ]
      )
    return msg.content


def generate_img_summaries(folder_path):
    folder_paths = [f"{folder_path}/{f}" for f in os.listdir(folder_path)]
    img_base64_list = []

    image_summaries = []
    for path in folder_paths:

        prompt = """You are an assistant tasked with summarizing images for retrieval. \
        These summaries will be embedded and used to retrieve the raw image. \
        Give a concise summary of the image that is well optimized for retrieval."""

        for img_file in sorted(os.listdir(path)):
            if img_file.endswith(".jpg"):
                img_path = os.path.join(path, img_file)
                base64_image = encode_image(img_path)
                img_base64_list.append(base64_image)
                image_summaries.append(image_summarize(base64_image, prompt))
                time.sleep(3)

    return img_base64_list, image_summaries

def generate_tab_summaries(tab):
    
    prompt_text = """You are an assistant tasked with summarizing tables for retrieval. \
        These summaries will be embedded and used to retrieve the raw table elements. \
        Explain and give a summary of the table that is well optimized for retrieval. Table {element} """
        
    prompt = PromptTemplate(template=prompt_text, input_variables=["element"])
    summarize_chain = {"element": lambda x: x} | prompt | GoogleGenerativeAI(model="models/text-bison-001", temperature=0) | StrOutputParser()
    table_summaries = summarize_chain.batch(tab,{"max_concurrency": 9})
    return table_summaries