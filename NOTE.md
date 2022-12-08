# Study Note

## 2022-12-07, WED.
### Today's contents:
* Extra Models/Multiple Models, and so on.
  * https://fastapi.tiangolo.com/ko/tutorial/extra-models/
  * https://fastapi.tiangolo.com/ko/tutorial/response-status-code/#_1
  * https://fastapi.tiangolo.com/ko/tutorial/request-forms/
  * https://fastapi.tiangolo.com/ko/tutorial/request-files/
* Testing

### Tips/Notes
* '*When defining a Union, include the most specific type first, followed by the less specific type. In the example below, the more specific PlaneItem comes before CarItem in Union[PlaneItem, CarItem].*'
  * 'Union' 이용시 먼저 오는 원소가 높은 우선순위를 가진다고.
* '*But if we put that in response_model=PlaneItem | CarItem we would get an error, because Python would try to perform an invalid operation between PlaneItem and CarItem instead of interpreting that as a type annotation.*'
  * Python 3.10에서도 'response_model'의 type을 설정하려면 'Union'을 이용해야한다.
* '*Response with arbitrary dict:<br>
You can also declare a response using a plain arbitrary dict, declaring just the type of the keys and values, without using a Pydantic model.
This is useful if you don't know the valid field/attribute names (that would be needed for a Pydantic model) beforehand.*'
  * 임의의 dict(dictionary)를 response model로 사용할 수 있다.
* '*응답 모델과 같은 방법으로, 어떤 경로 작동이든 status_code 매개변수를 사용하여 응답에 대한 HTTP 상태 코드를 선언할 수 있습니다.*'
  * '*status_code 는 "데코레이터" 메소드(get, post 등)의 매개변수입니다. 모든 매개변수들과 본문처럼 경로 작동 함수가 아닙니다.*'
  * '*status_code 는 파이썬의 http.HTTPStatus 와 같은 IntEnum 을 입력받을 수도 있습니다.*'
* '*하지만 모든 상태 코드들이 무엇을 의미하는지 외울 필요는 없습니다. fastapi.status 의 편의 변수를 사용할 수 있습니다.*'
* '*폼의 데이터는 파일이 포함되지 않은 경우 일반적으로 "미디어 유형" application/x-www-form-urlencoded 을 사용해 인코딩 됩니다.
하지만 파일이 포함된 경우, multipart/form-data로 인코딩됩니다. File을 사용하였다면, FastAPI는 본문의 적합한 부분에서 파일을 가져와야 한다는 것을 인지합니다.
인코딩과 폼 필드에 대해 더 알고싶다면, POST에 관한MDN웹 문서(아래 링크)를 참고하기 바랍니다.*' ...<br>
'*다수의 File 과 Form 매개변수를 한 경로 작동에 선언하는 것이 가능하지만, 요청의 본문이 application/json 가 아닌 multipart/form-data 로 인코딩 되기 때문에 JSON으로 받아야하는 Body 필드를 함께 선언할 수는 없습니다.
이는 FastAPI의 한계가 아니라, HTTP 프로토콜에 의한 것입니다.*'
  * https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST