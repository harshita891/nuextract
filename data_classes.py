from dataclasses import dataclass

@dataclass
class ExtractedInfo:
    company_name: str
    role: str
    duration: str
    stipend: str
    start_date: str
    end_date: str

@dataclass
class ExtractionResult:
    text: str
    extracted_info: ExtractedInfo
