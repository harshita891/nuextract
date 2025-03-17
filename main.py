from tqdm import tqdm
from extractor import NuExtractModel
from data_utils import load_json, save_json
from data import INPUT_FILE, OUTPUT_FILE, JSON_TEMPLATE
from logger import get_logger

logger = get_logger(__name__)

def process_in_batches(input_file, output_file, batch_size=35):
    try:
        data = load_json(input_file)
        texts = [entry["text"] for entry in data]

        extractor = NuExtractModel()
        results = []

        for i in tqdm(range(0, len(texts), batch_size), desc="Processing Batches"):
            batch_texts = texts[i : i + batch_size]
            batch_results = [extractor.extract(text, JSON_TEMPLATE) for text in batch_texts]
            results.extend(batch_results)

            save_json(results, output_file)
            logger.info(f"Processed {i + len(batch_texts)} texts so far.")

        logger.info(f"Extraction completed. Results saved in {output_file}")

    except Exception as e:
        logger.error(f"Processing failed: {e}")

if __name__ == "__main__":
    process_in_batches(INPUT_FILE, OUTPUT_FILE, batch_size=5)
