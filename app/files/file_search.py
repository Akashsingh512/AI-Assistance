import os

class FileSearch:
    @staticmethod
    def search_files(directory: str, keyword: str = "", extension: str = "") -> list:
        results = []
        if not os.path.exists(directory) or not os.path.isdir(directory):
            return results

        keyword_lower = keyword.lower()
        extension_lower = extension.lower() if extension else ""

        for root, _, files in os.walk(directory):
            for file in files:
                file_lower = file.lower()
                
                # Check extension first if provided
                if extension_lower and not file_lower.endswith(extension_lower):
                    continue
                    
                # Check keyword
                if keyword_lower and keyword_lower not in file_lower:
                    continue
                    
                results.append(os.path.join(root, file))
                
        return results
