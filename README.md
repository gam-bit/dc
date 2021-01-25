# 2020 DACON CUP

https://dacon.io/competitions/official/235683/overview/

- 대회 기간 : 2020.12.18 ~ 2021.01.22.17:59
- 실제 수행 기간 : 2020.12.28 ~ 2021.01.22
- 팀 : yonom unit -강김최
- 내용 : 시계열 분석


# 개요 

## 주제
과거의 데이콘 데이터를 활용한 미래의 사용자 행동 패턴을 예측

## 배경
데이콘은 전체 회원 약 2만명, 약 3만 회의 대회 참여, 47개의 공식 대회 개최, 총 상금 3억 7천만원이라는 국내 최대 규모의 인공지능 컴피티션 플랫폼이다. 2020년 한 해를 마무리하며 데이콘의 사용자 행동 데이터를 바탕으로 사용자 행동 패턴을 예측한다.

## 일정
- 우승 후보 코드 제출 : 2021년 01월 22일 ~ 2021년 01월 25일
- 우승 후보 코드 평가 : 2021년 01월 25일 ~ 2021년 01월 29일

※ 본 대회는 1월 29일 오후 6시에  최종  우승팀을 초청하여 온라인 발표를 진행할 예정입니다.


# 규칙

## 평가
- 심사 기준 : `Weighted RMSE`

    사용자 수, 세션 수, 신규 방문자 수, 페이지 뷰 수 4가지 항목을 예측한다. 각 변수의 크기가 다르기 때문에 가중치를 부여한 RMSE로 모델 성능을 평가한다.
    
```shell
def dacon_rmse(true, pred):
    # true.shape // (N,4)
    # pred.shape // (N,4)
    # w0, w1, w2, w3 <= train.csv의 사용자 수, 세션 수, 신규 방문자 수, 페이지 뷰 수 4가지 항목별 평균값
    score = np.sqrt(np.mean(np.square(true[:,0] - pred[:,0]))) / w0 +\
            + np.sqrt(np.mean(np.square(true[:,1] - pred[:,1]))) / w1 +\
            + np.sqrt(np.mean(np.square(true[:,2] - pred[:,2]))) / w2 +\
            + np.sqrt(np.mean(np.square(true[:,3] - pred[:,3]))) / w3 +\
     return score
```

- Public Score(리더보드 점수): 2020년 11월 9일 ~ 2020년 12월 8일의 일 단위 합계 데이터로 채점 → 평가 반영X
- Private Score: 2020년 12월 9일 ~ 2021년 1월 8일의 일 단위 합계 데이터로 채점 → 최종 평가에 반영
- 참가자는 제출 창에서 자신이 최종적으로 채점 받고 싶은 파일을 선택해야 함. (최종 파일 미선택시 처음으로 제출한 파일로 자동 선택됨)
- 대회 직후 공개되는 Private Score 랭킹은 최종 순위가 아니며, 유저 평가 코드 검증 후 최종 수상자가 결정됨


## 개인 또는 팀 참여 규칙

- 팀 최대 인원: 3명 
- 팀 구성은 본 대회 시작일부터 01월 11일까지 가능
- 팀원들의 제출 수의 합이 36 회(대회 경과일 12일 x 일일 최대 제출 수 3회) 이상인 경우 팀 병합 불가
- 팀 구성 시 각 팀원은 적어도 1회 제출 기록이 있어야 함
- 팀 구성 직후에는 팀원이 제출한 결과 중 가장 좋은 점수 공유
- 리더만이 팀원 추가와 결과물 제출 가능


# 데이터 

- 총 2차례에 걸쳐 제공 

## 1. 2020년 12월 18일 오후 5시 공개

- train.csv
    ```
    (2018년 9월 9일 ~ 2020년 11월 8일) 기간 동안 기록된 한 시간 간격의 사용자 행동 데이터
    
    > columns : 사용자 수, 세션 수, 신규 방문자 수, 페이지 뷰 수
    ```

- submission.csv
    ```
    모두 0으로 채워진 (2020년 11월 9일 ~ 2021년 1월 8일)의 일 단위 데이터
    
    > column : 사용자 수, 세션 수, 신규 방문자 수, 페이지 뷰 수
    ```
- info_user.csv (유저 정보)
- info_login.csv (로그인 정보)
- info_competition.csv (대회 정보)
- info_submission.csv (코드 제출 정보)



## 2. 2021년 1월 18일 오후 1시 공개
- 2차_train.csv
    ```
    (2020년 11월 9일 ~ 2020년 12월 8일) 기간 동안 기록된 한 시간 간격의 사용자 행동 데이터
    column : 사용자 수, 세션 수, 신규 방문자 수, 페이지 뷰 수
    ```

# 사용한 모델

- RandomForest
    
    > - 랜덤 포레스트는 변수로 input time step의 모든 값이 들어가게 되면서 시간 정보를 손실
    > - y값들은 시간이 흐르면서 전반적으로 값이 증가하고 있음. 그러나 랜덤 포레스트는 `y의 예측값 = 마지막 leaf의 y값들의 평균`이라서 그래프를 벗어나는 y값을 예측하지 못 함. → 딥러닝 사용하기로 함  

- LSTM
- GRU
- SEQ2SEQ
- facebook prophet

## 선택한 모델
- LSTM + facebook prophet 앙상블



# pipline

- 분석
- 모델링(전처리 + 모델링 + 예측 시각화)
    - 전처리
        - hyperparameter : input, output의 sequence 길이
        - 즉, 몇 일을 넣고 몇 일을 예측할지를 결정해야 함
    - 모델링
        - hyperparameter : 레이어 수, hidden_size, epochs, lr 
- Validation
    - 시계열 예측에서는 일반적으로 시행하는 cross-validation으로 validation을 사용하면 안 됨. time step에 맞추어서 train-test set을 split하는 `walk-forward validation`을 사용.
    ![image](https://user-images.githubusercontent.com/58651942/105652357-5eca0700-5efc-11eb-91c3-79d7b19c5b9f.png)

