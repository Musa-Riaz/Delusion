import os
import shutil
import file_paths as fp
from indexer import index_csv_dataset
from sorter import sort_all_barrels

def clean_and_index():
    # 1. Clear old indexes
    folders_to_clean = ['indexes', 'indexes/forward_index', 'indexes/inverted_index']
    files_to_clean = [
        fp.lexicon_file, fp.ids_file, fp.indexed_urls_file, 
        fp.frequencies_file, fp.texts_file + '.csv', 
        fp.texts_file + '.bin', fp.scraped_file + '.csv'
    ]
    
    print("🧹 Cleaning and initializing index files...")
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)
        
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            os.remove(file_path)
            
    # 2. Initialize essential empty files to prevent IOErrors
    # The indexer needs 'texts.csv' to already exist to calculate offsets
    with open(fp.texts_file + '.csv', 'w', encoding='utf-8') as f:
        pass
    with open(fp.scraped_file + '.csv', 'w', encoding='utf-8') as f:
        pass

    # 3. Run Indexing
    print("\n--- Phase 1: Bulk Indexing (30 Articles) ---")
    try:
        index_csv_dataset(
            fp.dataset_file, 
            fp.lexicon_file, 
            fp.ids_file, 
            fp.forward_index_folder, 
            fp.indexed_urls_file, 
            fp.processed_docs_file, 
            is_new_doc=False
        )
    except Exception as e:
        print(f"❌ Error during indexing: {e}")
        return

    # 4. Run Sorting
    print("\n--- Phase 2: Sorting Barrels ---")
    sort_all_barrels()
    print("\n✅ Setup Complete! You can now run 'python server.py'.")

if __name__ == "__main__":
    clean_and_index()
