##### 해당 프로젝트는 큐톤 신호(광고)가 들어올 때 해당 신호가 이상신호인지 정상신호인지 판단하는 모델과 시스템을
##### 구축하는 프로젝트입니다. 해당 프로젝트는 이상신호, 정상신호에 대한 정의 혹은 규칙이 따로 존재하지 않기 때문에
##### 연구원의 역량으로 정상, 이상 유무를 근거를 바탕으로 판단해야 하는 프로젝트입니다. 




## Data 폴더 
- data_preprocess : dataset안에 있는 데이터들을 전처리 하여 data_preprocess 안에 저장 
- dataset : 원시 데이터이외에도 data_process, Experiment에서 파생된 데이터 들을 저장

## Experiment 폴더 
- data_preprocess에서 전처리가 완료 되어 dataset폴더로 저장되면 해당 폴더에서 데이터를 불러와서 실험을 진행함

## Library 폴더
- 직접 만든 라이브러리나 Kobert와 같은 모델을 레퍼런스 할때 사용함

## Model 폴더
- Experiment에서 사용한 모델을 저장함
