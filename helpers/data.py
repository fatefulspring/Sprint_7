BASE_URL = 'https://qa-scooter.praktikum-services.ru'

COURIER_MESSAGE_INVALID_LOGIN = {
    "code": 409,
    "message": "Этот логин уже используется. Попробуйте другой."
}
COURIER_MESSAGE_EMPTY_FIELD = {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}
COURIER_MESSAGE_LOGIN_NOT_FOUND = {'code': 404, 'message': 'Учетная запись не найдена'}
COURIER_MESSAGE_EMPTY_LOGIN = {'code': 400, 'message': 'Недостаточно данных для входа'}

ORDER_CREATE_PAYLOAD = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha",
}
ORDER_LIST_KEYS = {'id', 'courierId', 'firstName', 'lastName', 'address', 'metroStation', 'phone',
                   'rentTime',
                   'deliveryDate', 'track', 'color', 'comment', 'createdAt', 'updatedAt', 'status'}

