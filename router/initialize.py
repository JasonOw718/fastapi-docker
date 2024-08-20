from fastapi import APIRouter
from init.extract_doc import extract_doc
from init.generate_summary import generate_img_summaries,generate_tab_summaries

router = APIRouter(
    prefix="/init",
    tags=["INITIALIZATION"]
)

@router.post("/initialize")
def init():
    print("Extracting docs...")
    Header, Footer, Title, NarrativeText, Text, ListItem, img, tab= extract_doc("./docs")
    print("Document extracted...")
    print("Generating table summaries...")
    rable_summaries = generate_tab_summaries(tab)
    print("Table Summary Generated...")
    print("Generating image summaries...")
    img_base64_list, image_summaries = generate_img_summaries("./extracted_data")
    print("Image Summary Generated...")

