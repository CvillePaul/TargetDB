python .\manage.py ClearDatabase

@rem python .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202305\*.nor" "Data Files\SpectrumRawData\LBT Spectra 2023-05" QuadEB
@rem python .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202306\*.nor" "Data Files\SpectrumRawData\LBT Spectra 2023-06" QuadEB
@rem python .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202309\*.bwl" "Data Files\SpectrumRawData\LBT Spectra 2023-09" QuadEB
@rem python .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202310\*.bwl" "Data Files\SpectrumRawData\LBT Spectra 2023-10" QuadEB
@rem python .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202312\*.bwl" "Data Files\SpectrumRawData\LBT Spectra 2023-12" QuadEB

python .\manage.py LoadPerson             "Data Files\People.csv"
python .\manage.py LoadTargetIdType       "Data Files\TargetIdTypes.csv"
python .\manage.py LoadTarget             "Data Files\Targets.csv"
python .\manage.py LoadTargetList         "Data Files\Target Lists\*.csv"
python .\manage.py LoadObservatory        "Data Files\Observatories.csv"
python .\manage.py LoadObservingProgram   "Data Files\ObservingPrograms.csv"
python .\manage.py LoadObservationPurpose "Data Files\ObservationPurposes.csv"
python .\manage.py LoadSpectrumRawData    "Data Files\SpectrumRawData\LBT Spectra *.csv"
python .\manage.py LoadSpeckleRawData     "Data Files\SpeckleRawData.csv"

