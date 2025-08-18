from pydantic import BaseModel, Field

# Field with descriptions → helpful in Swagger docs & self-documentation.
# Validation rules → 
### ge=0 (greater or equal to 0) for values that can’t be negative.
### Age: ge=1 since age must be at least 1.


class PatientData(BaseModel):
    Pregnancies: int = Field(..., description="Number of times pregnant", ge=0)
    Glucose: int = Field(..., description="Plasma glucose concentration (mg/dL)", ge=0)
    BloodPressure: int = Field(..., description="Diastolic blood pressure (mm Hg)", ge=0)
    SkinThickness: int = Field(..., description="Triceps skinfold thickness (mm)", ge=0)
    Insulin: int = Field(..., description="2-Hour serum insulin (mu U/ml)", ge=0)
    BMI: float = Field(..., description="Body Mass Index (weight in kg/(height in m)^2)", ge=0)
    DiabetesPedigreeFunction: float = Field(..., description="Diabetes pedigree function score", ge=0)
    Age: int = Field(..., description="Age in years", ge=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Pregnancies": 2,
                    "Glucose": 120,
                    "BloodPressure": 70,
                    "SkinThickness": 25,
                    "Insulin": 85,
                    "BMI": 28.5,
                    "DiabetesPedigreeFunction": 0.627,
                    "Age": 32
                }
            ]
        }
    }











# from pydantic import BaseModel

# class PatientData(BaseModel):
#     Pregnancies: int
#     Glucose: int
#     BloodPressure: int
#     SkinThickness: int
#     Insulin: int
#     BMI: float
#     DiabetesPedigreeFunction: float
#     Age: int



