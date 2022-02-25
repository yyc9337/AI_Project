## data 폴더 
- data_preprocess : dataset안에 있는 데이터들을 전처리 하여 data_preprocess 안에 저장 
- dataset : 원시 데이터이외에도 data_process, Experiment에서 파생된 데이터 들을 저장

## Experiment 폴더 
- data_preprocess에서 전처리가 완료 되어 dataset폴더로 저장되면 해당 폴더에서 데이터를 불러와서 실험을 진행함

## Library 폴더
- 직접 만든 라이브러리나 Kobert와 같은 모델을 레퍼런스 할때 사용함

## Model 폴더
- Experiment에서 사용한 모델을 저장함