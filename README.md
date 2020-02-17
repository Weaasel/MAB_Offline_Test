# MAB 모델 오프라인 테스트를 위한 환경 구축

## 구성
simulator 클래스에 세팅(포지션 별 관측 확률, 아이템 별 관측 시 클릭될 조건부 확률)을 준 뒤 run을 실행하면 해당 세팅에서 각 모델(Thompson Sampling, UCB1,  Random, etc.)의 행동을 시뮬레이션 한 뒤 결과를 저장한다.

## MAB 클래스
* MAB 모델이 얻을 수 있는 정보는 아이템의 id와 포지션 별 유저의 관측 확률뿐이다.

* MAB의 select_items 함수를 뽑아야 할 아이템의 개수를 인자로 넘겨주며 호출하면, MAB는 이때까지 얻은 정보를 토대로 item id의 리스트를 반환해야 한다. 이 때 반환되는 리스트에서 아이템 아이디의 인덱스가 해당 아이템이 노출될 포지션을 뜻한다.

* MAB의 update 함수에 MAB가 select_items의 결과로 반환한 리스트와, 해당 리스트에 대한 유저 피드백 리스트(list of boolean, k번째 인덱스의 값이 True면 유저가 해당 위치의 아이템을 클릭한 것이고 False면 관측 후 무시했거나 관측하지 않은 것)를 인자로 호출하면 MAB는 내부 정보를 업데이트한다.

## 클래스 및 변수 의미
* K : 가능한 아이템의 개수

* L : 가능한 포지션의 개수

* posProb : posProb[i]는 i번째 포지션을 유저가 관측할 확률. 가능한 인덱스는 [0, L-1]

* itemProb : itemProb[idx][i]는 i번 아이템의 idx번 구간의 step에서 관측됐을 때 유저가 클릭할 확률. 가능한 인덱스는 [0, intervals-1][0, K-1]

* S : 크기 K의 1차원 배열. S[k]는 k번째 아이템이 유저에게 클릭된 횟수이다.

* N : 크기 K의 1차원 배열. N[k]는 k번째 아이템이 노출된 횟수이다(유저가 관측했는지 여부는 상관 없음).

## 예정 사항
* 추가 개선사항:
	1. 현재 position별 노출 확률인 posProb을 사용하고 있는데, 우리 서비스에서는 position별 노출 확률은 딱히 정해져 있지 않으므로 [1.0] * # of items 로 세팅했음. 즉 필요가 없음. 그런데 현재 코드에서는 selected_arms_nums를 세팅할 때 역할을 해주기 때문에 바로 뺄 수 없음. posProb을 빼는 방향으로 코드 수정 예정.

	2. 현재 우리 서비스에 맞는 non-stationary bandit의 구현을 위해 itemProb을 2차원 배열로 선언하였는데, 효과적인 관리를 위해 함수 형태를 갖도록 수정할 필요가 있음. (ex. 일차함수의 parameter 부여)
	
	3. 우리 서비스에서는 reward가 한 item에만 적용되도록 함. 즉 한 item이 click되면 다른 item들에게는 기회가 없음.  
  이 부분을 반영하여 코드 수정 예정.
	
	4. Aurochs.app에서 사용하는 vimp 환경 구축  
	뽑은 position 이하의 item만 N을 up 할 수 있도록 코드 수정 예정.
  
## 실험 결과 예시(regretion)
<img width="400" alt="I-CTR" src="https://github.daumkakao.com/weasel-lee/personal_issues/blob/master/%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D/MAB_Offline_test/2020-02-17-02-02-30.graph_without_random.png?raw=true">  

