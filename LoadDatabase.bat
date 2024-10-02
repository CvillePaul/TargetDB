py .\manage.py ClearDatabase

@rem py .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202305\*.nor" "Data Files\SpectrumRawData\LBT Spectra 2023-05" QuadEB
@rem py .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202306\*.nor" "Data Files\SpectrumRawData\LBT Spectra 2023-06" QuadEB
@rem py .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202309\*.bwl" "Data Files\SpectrumRawData\LBT Spectra 2023-09" QuadEB
@rem py .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202310\*.bwl" "Data Files\SpectrumRawData\LBT Spectra 2023-10" QuadEB
@rem py .\manage.py MakeSpectrumRawDataCsv "..\..\Files\202312\*.bwl" "Data Files\SpectrumRawData\LBT Spectra 2023-12" QuadEB

py .\manage.py LoadPerson             "Data Files\People.csv"
py .\manage.py LoadTargetIdType       "Data Files\TargetIdTypes.csv"
py .\manage.py LoadTarget             "Data Files\Targets\*.csv"
py .\manage.py LoadCatalogAssociation "Data Files\Catalog Associations\*.csv"
py .\manage.py LoadCatalogData
py .\manage.py LoadTargetList         "Data Files\Target Lists\*.csv"
py .\manage.py LoadObservatory        "Data Files\Observatories.csv"
py .\manage.py LoadObservingProgram   "Data Files\ObservingPrograms.csv"
py .\manage.py LoadObservationPurpose "Data Files\ObservationPurposes.csv"
py .\manage.py LoadSpectrumRawData    "Data Files\SpectrumRawData\LBT Spectra *.csv"
py .\manage.py LoadSpeckleRawData     "Data Files\SpeckleRawData.csv"
py .\manage.py LoadBinaryParameters   ".\Data Files\Binary Parameters\*.csv"
