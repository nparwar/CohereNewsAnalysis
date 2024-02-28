import cohere
from dotenv import load_dotenv
import os

def classify_Data(df):
    #This first part finetunes the data
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    # create dataset
    dataset_name = "article_title_dataset_2024"
    model_name = "fina_article_classification_2024"

    # Check if the dataset already exists
    existing_datasets = co.list_datasets()
    if any(dataset.name == dataset_name for dataset in existing_datasets):
        print(f"Dataset '{dataset_name}' already exists. No need to upload again.")
    else:
        single_label_dataset = co.create_dataset(name="article_title_dataset_2024",
                                            data=open("all-data.csv", "rb"),
                                            dataset_type="single-label-classification-finetune-input") 
        print(single_label_dataset.await_validation())
                                                
    # start the fine-tune job using this dataset
    existing_models = co.list_custom_models()
    if any(model.name == model_name for model in existing_models):
        print(f"Model '{model_name}' already exists. No need to fine-tune again.")
    else:
        finetune = co.create_custom_model(
        name="fina_article_classification_2024", 
        dataset=single_label_dataset,
        model_type="CLASSIFY"
        )
        finetune.wait() # this will poll the server for status updates
        print(f"fine-tune ID: {finetune.id}, fine-tune status: {finetune.status}")

    # get the custom model object
    ft = co.get_custom_model("967de23a-5649-4313-ab94-be58d966731f")

    response = co.classify(
        inputs=df["Title"].tolist(),
        model=ft.model_id,
    )
    df['Sentiment'] = [classification.predictions[0] for classification in response.classifications]
    return df