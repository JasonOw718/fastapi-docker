from unstructured.partition.pdf import partition_pdf
import os

def extract_doc(pdf_folder):
    Header, Footer, Title, NarrativeText, Text, ListItem, img, tab = [], [], [], [], [], [], [], []
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    index = 0
    # Loop through each PDF file and apply the partition_pdf function
    for pdf_file in pdf_files:
        index +=1
        pdf_path = os.path.join(pdf_folder, pdf_file)
        
        # Extract content from the PDF
        raw_pdf_elements = partition_pdf(
            filename=pdf_path,
            strategy="hi_res",
            extract_images_in_pdf=True,
            extract_image_block_types=["Image", "Table"],
            extract_image_block_to_payload=False,
            extract_image_block_output_dir=f"extracted_data/pdf-{index}"
        )
        
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Header" in str(type(element)):
            Header.append(str(element))
        elif "unstructured.documents.elements.Footer" in str(type(element)):
            Footer.append(str(element))
        elif "unstructured.documents.elements.Title" in str(type(element)):
            Title.append(str(element))
        elif "unstructured.documents.elements.NarrativeText" in str(type(element)):
            NarrativeText.append(str(element))
        elif "unstructured.documents.elements.Text" in str(type(element)):
            Text.append(str(element))
        elif "unstructured.documents.elements.ListItem" in str(type(element)):
            ListItem.append(str(element))
        elif "unstructured.documents.elements.Image" in str(type(element)):
            img.append(str(element))
        elif "unstructured.documents.elements.Table" in str(type(element)):
            tab.append(str(element))
            
    return Header, Footer, Title, NarrativeText, Text, ListItem, img, tab