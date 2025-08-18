from pydantic import BaseModel, Field

class PatientData(BaseModel):
    Pregnancies: int = Field(..., description="Number of times pregnant", ge=0)
    Glucose: int = Field(..., description="Plasma glucose concentration (mg/dL)", ge=0)
    BloodPressure: int = Field(..., description="Diastolic blood pressure (mm Hg)", ge=0)
    SkinThickness: int = Field(..., description="Triceps skinfold thickness (mm)", ge=0)
    Insulin: int = Field(..., description="2-Hour serum insulin (mu U/ml)", ge=0)
    BMI: float = Field(..., description="Body Mass Index (weight in kg/(height in m)^2)", ge=0)
    DiabetesPedigreeFunction: float = Field(..., description="Diabetes pedigree function score", ge=0)
    Age: int = Field(..., description="Age in years", ge=1)