# 💊 Medical Prescription and Drug Leaflet Simplifier

### An NLP-Based Application with OCR, Dosage and Warning Extraction, Verification and Readability Scoring

## 📌 About the Project

The **Medical Prescription and Drug Leaflet Simplifier** is an NLP-based application designed to make complex medical prescriptions and drug leaflet information easier to understand.

The system extracts important medical information, including drug name, strength, dosage, frequency, duration, warnings, and side effects. It simplifies complex medical instructions into easy-to-understand language and checks whether critical information is preserved.

The application also supports prescription image and PDF uploads using Optical Character Recognition (OCR).

## 🎯 Objectives

- Extract important medical information from prescription documents.
- Identify drug names, strengths, dosage, frequency, and duration.
- Extract warnings and possible side effects.
- Simplify complex medical text into easy language.
- Verify the preservation of critical information.
- Evaluate text readability.
- Support image and PDF uploads through OCR.
- Process multiple documents through batch processing.
- Generate downloadable CSV reports.

## ✨ Key Features

- **Medical Information Extraction:** Extracts seven important medical fields using rule-based NLP and regular expressions.
- **Text Simplification:** Converts complex medical instructions into simpler language.
- **OCR Support:** Extracts text from JPG, JPEG, and PNG images.
- **PDF Processing:** Supports both digital PDFs and scanned PDFs.
- **Image Preprocessing:** Uses grayscale conversion, contrast enhancement, cropping, enlargement, and sharpness enhancement.
- **Information Verification:** Checks whether critical information is preserved during simplification.
- **Extraction Quality Assessment:** Identifies detected and missing fields and calculates completeness percentage.
- **Readability Scoring:** Uses Textstat to evaluate text readability.
- **Batch Processing:** Processes up to five documents in one batch.
- **CSV Report Generation:** Allows users to download batch-processing results.
- **Web Dashboard:** Provides an interactive interface using Flask, HTML, and CSS.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| NLP | Medical text processing |
| Regular Expressions | Information extraction |
| Tesseract OCR | Text recognition |
| PyTesseract | Python OCR integration |
| Pillow | Image preprocessing |
| PyMuPDF | PDF rendering and scanned PDF processing |
| pypdf | Digital PDF text extraction |
| Textstat | Readability assessment |
| HTML | Frontend structure |
| CSS | Frontend styling |
| CSV | Report generation |

## 📂 Project Structure

```text
Medical_Prescription_Simplifier/
│
├── data/
│   └── raw/
│       └── medical_dataset.csv
│
├── src/
│   ├── extraction.py
│   ├── simplification.py
│   ├── verification.py
│   ├── advanced_verification.py
│   ├── ocr_engine.py
│   ├── document_upload.py
│   ├── batch_processor.py
│   ├── app.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       └── style.css
│
├── evaluation/
│   └── evaluate.py
│
├── create_dataset.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Priyankagitkumarihubbit784/Medical-Prescription-Simplifier.git
```

### 2. Navigate to the Project Directory

```bash
cd Medical-Prescription-Simplifier
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Tesseract OCR

Tesseract OCR must be installed separately.

Download it from:

https://github.com/UB-Mannheim/tesseract/wiki

Make sure the Tesseract executable path is configured correctly in `src/ocr_engine.py`.

### 7. Run the Application

```bash
python -m src.app
```

Open your browser and visit:

http://127.0.0.1:5000

## 🔄 System Workflow

```text
User Input
    |
    v
Manual Text / Image / PDF Upload
    |
    v
Document Processing and OCR
    |
    v
Text Preprocessing
    |
    v
Medical Information Extraction
    |
    v
Text Simplification
    |
    v
Critical Information Verification
    |
    v
Extraction Quality Assessment
    |
    v
Readability Assessment
    |
    v
Flask Dashboard
    |
    v
Results and CSV Report
```

## 🧪 Testing

The following functionalities were tested during development:

- Medical information extraction
- Text simplification
- Critical information verification
- Readability assessment
- Image OCR
- Digital PDF text extraction
- Scanned PDF OCR
- Extraction quality assessment
- Batch document processing
- CSV report generation
- Flask web application

A synthetic sample prescription was successfully processed, with all seven expected fields detected.

## 📊 Dataset

- Dataset: `medical_dataset.csv`
- Number of records: 15
- Type: Synthetic medical prescription examples
- Purpose: Testing and demonstration

The dataset contains fictional examples and does not contain real patient prescriptions.

## ⚠️ Limitations and Medical Disclaimer

This project is an educational prototype developed for learning and demonstration purposes.

- OCR may produce incorrect or incomplete text.
- Rule-based extraction may not recognize every medical format.
- Extraction completeness does not guarantee extraction accuracy.
- Verification is heuristic and has not been clinically validated.
- All extracted medicine names, strengths, dosages, durations, and warnings must be checked against the original document.

**This application is not a substitute for a doctor, pharmacist, or professional medical advice. Do not use its output to make medication decisions without professional verification.**

## 🚀 Future Enhancements

- Integration of transformer-based NLP models.
- Advanced medical Named Entity Recognition.
- Multilingual medical text simplification.
- Improved OCR accuracy.
- Semantic verification of medical information.
- Larger validated medical datasets.
- Secure document storage and user authentication.
- Mobile application development.

## 👩‍💻 Developer

**Priyanka Tiwari**

MCA (Artificial Intelligence and Machine Learning)

Chandigarh University

## ⭐ Acknowledgement

This project was developed as an academic project to explore the applications of Natural Language Processing, OCR, and text simplification in healthcare-related document processing.

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.