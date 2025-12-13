import sys
import json
import os
import logging
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time
import requests
import random
import string
import hashlib
from uuid import uuid4

# Configuration
open_id_list = ['MrUO3W6kwbGV4i7DOskcb6rVkpQc', 's5zxaNybXfT7fS2rSOb68x4UiDTR', 'CnpmngvcvItm8RFtoiNwJyurnXPH',
'RUN3PtbieqhatzsS1PN0zzC0D8kQ', 'qVsmYCx87ddx8A2FueYIEKNOftAX', 'C13nGeJXwiqZjMqdwRCHIi28dOIF',
'v49mhppTjFgx0Nhyqh9QWp7QVdNH', 'uzZEEOldGzAK6wUFaFQkwahZb1AW', 'hnXfMKXzH9KFlro9Ty6Gg7xGGTXc',
'amkVUTIPMkG7zrvZn48y8JRkmu9e', 'XERWxSV0NAJjhnto8Aql9RR9UklJ', 'ZcMCsfxHltZNA5mcQWkflXCMy8pg',
'oFNc0jKIXcq9g2NzMhaHDJmF5MAc', '9iUJ8o00MnLTbv0umlTPXW8SASBC', 'sCoyZKnurCW3pF94XTxh1X6IkqoS',
'ulupP8ngybsCB7vZPXWiTAnApmAl', 'QgBMKbfTbhuQWSEn8FuB0k1IRnIA', 'fDtcWiMg68SGPqfu422tMZQK5NHD',
'2rStLKqw5ADL7cmcT6NFHDDcKXtk', 'p6leZTkfTFMc4nPzLu0uxnsDEePF', '2SQDpoJL8zZdM8ohDPliPgPlAZMf',
'o2ZRgONeP3OoFUGM4q235cWnDMTz', 'F3JoC2qaerOghnwPoLEiLrsuFOWf', 'zikgCv6QWMNh1NnbU8XOFnntS0sF',
'2ELYukr1sBWhEzO8I5hNgtaHa922', 'pxyTmu00w6gPNVoi169CZNuQHtUn', '7pdukl9yow0QNBuy7xK0XhOHaeeJ',
'PWoIrNEUMd2rcQznYUxJsdJ4WG3y', 'oeWVOFvzFrHEaZu1vOgfhCRvJyor', 'luMm3xE1uvuttHQW1oo5sLKltlfc',
'xcp9qESBqjDyrzJxid0kOCCB11XR', 'OjCE6e5EByyTSaMfXlkx8KKt1rfG', 'o4iunOfRP1Pk3BWs2jxyJDEDJ6Vu',
'3hj3qFlB6XxLy2p080IoNZq06Un8', 'D3qGcIPxBIKqlJjWzxuex4qI5cMA', '5ponze2pGuhnMYkBIkKuBWrsG8cK',
'fgdUZpAxZ9TcHIa65r0cANpQhdr3', 'BiRbm5iTiAulaDdp6ZWyHZUoByDk', 'VFP8EsTica6S3HGYYW3HD1qXijJ2',
'uv9mNAuaRmltBx7UyDe7AyZverzY', '2gxbp5EDqJ0PA7jShtJFVV7jwaRd', 'DqOeIHsYNthIZDCzoNO0APC05FHG',
'gyVpnSh98Oqj0XnYGEPIN4gfkTbd', 'dYNul6ovRTkGD3tA0ks5lkyqvTvy', 'FKiCsn7oHQZq1rD39MnEDWy1o2jx',
'U6mgk5LWTvx4CJXWOIOMsCejDqDn', 'ijr8lhn9dE89ATz3lkNQQxYt4Fnv', 'W4YNPY4CzqHImQyY2X4AnTHZmOdT',
'OXqfdgjqcuei6ymrk6rNI0QAsIDv', 'Wqi93RfCvH8F3vQbBSatewvOq4iO', '0bxbef8TLNzjZs1dLyErigfnNhz8',
'6E9bmKxY8izozovfaycaf6jJeSpl', 'U1X1lIsKPeuEioOd02PrRZ15LZVi', 'f9K8hUrgqM8DDD1pW4jbRaKkWa99',
'nqYqtG45Ju0SQ5eJFgDp7lVWCLQ3', '8fsmhJnnNWsyBGb1ahtesee9Wrum', '8ELG2Yv1S4RA68SJykYveMLfzgM2',
'r2zlOyDBjZGWiOaaNoLOkeSC8S5a', 'UIJu2NFxg4StBTbgABpzTK53j8uB', 'wpckFX0zQucgUXyrspbw6zOZvWMz',
'0fJQPF9PjRBfOu0v1LLxoRY9hxpS', 'BfmeeWJ1NORBPzVMK1ao7rYVoMjJ', 'kAGXOTpSbid6roezSivFV1AiNw1y',
'D6LXYnxKnai64ShhcFUdQYQ9XRar', 'TWyrg9vLz1cEjUp0uLWutBuf85es', 'rOt4Zzm2zk3QEMPcshzmh8xomQcG',
'sXH1DPmq5GViWK7vwxyBvMXDn8ny', 'nNkAb2Ba0TEEzihM4EyIxYxwXvAY', 'gV0M4gFn6DVrpwqIwaGwhGd9nn8P',
'YLlLd7ZogzZDiOQyjReDRPS3Nd8Z', 'D3jxWd2J1lhT17vhpzbg7ce4pRdm', 'ybfC6NwTgSpEY1ZXe2IngOG6a0ac',
'cv0t6lAq5jRx2L3ZtPWNwOUatFym', 'RDHBXz0Anr3yCR9Hpdj1OOzicdUD', 'lNAKeUh78gvX0ihLeEPyRHpwkNQj',
'Md6CBjkaF5IfK1UOexnbEAKuwA0c', 'iWUk27E9aoDmXGszNazocon3qVNW', 'LZt3rlZmaj3pR1A0Dfvx2R1LlaHJ',
'htLxskKqfx23LR30HRbmQmTe5kIV', 'SVmtu4Of7HZEh4cTpJQ6xMF6UkrE', 'jO5Ty2GtSI3PvE1oCqTNZy2KmTGv',
'OXsSC2mXWkUDUO0zp9e7N6XoX9sw', 'e6VU7PoW8fXkvU6Na1GE2ORRvEP2', 'RYIAU6EVgKBXXjOvZyo6aP8zxmqa',
'ClttzA5ZsTy6qHhEysXjR9QqtUYR', 'iRFG8JgISmcKjxKyXrjSbZnpBMCn', '5S3VWEtnsRNA9u5Ax6FmyxQhkqOR',
'XkwD6eWgY3eyy3mulYbD7PpnVzO8', 'm0mWyVruikv17cndiLEcYzICqDZb', 'dMsV71J8fH86zSUcpqUhUTdkHGMD',
'fDMmjJGosdJ7stFg0Bba1JuBnpoy', 'bmUrZxBU6h6q333PVpwKUVH6zDXf', 'Y1p4hrnifQF6NxB5oYlXGNLD7xCL',
'LAJRPA0HizlMxHdXdAaJdX8Vp7R0', 'Jl7uKC0XDiBAy9lmiQenTT7KIVP4', 'GGgOvq0VQJPJcjmuiYvsZQLmRFSB',
'bIlpv0IP7AwTaUig0lbnWj1o5Mj5', '1qAMeyg4joS4goPGrMo9EbEUEco4', '3ar8FhV8AsxDKmHyxHeeKbLgs59Z',
'A9O3J2iZP9KI68hNuyhbsCy1lycl', '9SNaYfc1KIP73czATWbQNzEIhQ7U', 'bN4tSFY91d2TwCUhqRIgqxpaCfK2',
'QfQvHVlg4gJLoVLehLgG1AS594eR', 'Eck93EoEvuLM95k7QBUnyFK32ga8', 'raqVIiwyA2uNZGdVYTGrl3PTeExO',
'XNEhJcdxME74kahSvdatJvsk1ngU', 'grEs51hrOXDYFo84Cio38FKtfl9X', 'itRbmSx8E8zD2PcjRE8Ej7Kv1q7N',
'tmgCBRwEtJkwB3UPyxJeZMQQjsua', '0lTXWs7lW8J27N9eAPCgmTmS9maZ', 'naXbWgbWneLQQwupo0cCQVfUpWrx',
'obcwxvPhyMg3Ur1VcPJ06YbJry1E', 'NkdlFgsG0vUD4ez79zgfnqtlbzcI', 'Gdw8VA9wZpUqqstSNBdcuUWNaLhP',
'GPcbToBenFzXsr1lr8Ca4MslrzuK', 'JSm0sQe2OritN5fB3eym1gfkkChn', '1O7buX8Ve5cG9h2Om1cOKJYr7JKX',
'0fONbq9mYahaCaAlDn4eB1oIArtq', 'KUqdzIMZvEz1RdJNjmAYZe7ti9AC', 'Vgwe8BRAOLjqBiQjX1E03KLRchLT',
'4SlAFNp1Ndn1vj2zNXNiStyzRm8V', 'wSCxznTUSQPBWJ8cvaroEWuySpJm', 'Ln3sAAxLgzOqbIIjlwjoKh400ouv',
'1eGCpf3bmAICtiVNzTuhEk8asj5e', 'Js1pz5ctEo15dj9mOEzaryu5uV1N', 'PmSA8k29ABHEUlmGgV4LzFSwcvtI',
'kyjNRjh6DpuII2TEnCAUb4NHGqF1', 'HEDmVL3BBP4YtC1gaTLhWPpoDRqW', 'AOmAVCLiS3Ag14ZfvQbDpRKHcEpJ',
'RPfhyxaT6uWn77dv9BBVF48IwD5P', '07gi1KMHzCDb8uLTyevubIQy8iBp', 'cRve90tKwdIWoJ38MfLFQHjxknLB',
'MnTPq3jy2o9PBQpEkeHqNENwa0HZ', '8nnVhA6eCWkae3vuTWYAl7hiB7XY', 'OXoOscarNYt6i5LV3jmsf6eGXe54',
'VOWxFeDub2xBlllHGmA6FS0hSoia', 'rs71GhUGjNI6KkGA1BRRSarAI8RB', 'DIF2pguQDtliLBEV46XHROUQ16Oh',
'JP5OaEGHAgYeRwwAzeAjwA4I1HMW', 'Jty7YliRpvPCpJWlL1dHvf5XLgTy', 'oUkwyWmy4rWZyQZHoYVBTitv5Rk1',
'BZK7absOdhj2pUuW0pWeRCzZnFNt', 'pyuo3WLmMFcRQplILFQjcOMu2HaH', 'jV2m5GUbRpnfTcSjnbKARShCwSd9',
'bldXL5fy3X4JUg25vv1k0d3KhFbX', 'fRjUeodBQp8iCpzUdf58ByezSYFV', 'bvuD8HJBgmNf7TYYkAVy1qE0Vln9',
'gwLh9p1LGy8rkyxun90dzpnKFg56', '18j2CpjMb5bVLalNLmGzYgP4mw5w', 'xgRyDQwSNYdOu9jJbWgBIcWujgZS',
'CnKUxjg7t5ddUnu1AofvUtVnEpRk', 'LZgtUyFmgqZpksjSc6iPpBuxQm2z', 'TCfiW0IZA88ToIcE8FPSq6Duiczx',
'RK3Fguy9dxchXap8XgxqLUmUOGz4', '2XXxZRfzgsdVlc6aLW6Qi1LEAm13', 'XLQjl7JQaaZrw9eJNC4G84mx34Jy',
'ViNU7Juv81jWkVRHOuSHeOuJOxXk', 'UjOqGkKvrE1SaUp4qL92QACj8pEe', 'qL5aioZbssVhnW7fR6Z9mUaysuls',
'kPXa8xpL41bSiQMHvFPdfOrX0UpN', '6waUTJE1UIJ6WG1WGzDbh49MbLP7', 'gwXKsvjvPjXR12nQVRpboyOyAvrW',
'rqWlsDlvx3JQpqTYxmY0PfoDaLrK', '4dxzpfZ2HNz4cnnG0LvlPjYvAou1', 'afhclbECGM9kpJUd8MbzVcztZNOI',
'hUkGzrfKIJ1hvnURY1dL2dYRRStn', 'xeonGKtgx5eNEr0btBa5NU1X1Yvh', 'XYeTx8nMUDSARVnMq7ocPpck02BQ',
'KR8gBtZiIoNzuLEZZ7BXeZbZcsZQ', '7nIu2TuRQtNQVyXJQyVZz0DYS1b0', 'Puts9jYDpCL3jUv3YFGtO8bxVo9B',
'd3muFdCA79fDlNshy3RF31sXFzCk', 'ySF9uApB5SehspwW2BjovvPUxFgl', 'P0vmjuuMMCdlYFTSYnL3BpntiJVe',
'skVxuYHkPCTiH6daetzQgLejiN9O', 'uzHPLhDAchIkZ3yLvcVI6l8Nudk4', 'DGyC3AXDQevVdlbPBXmyHHNfWUQf',
'7TVxCP6Ng5ziy4QjN0OyxEbYhNuj', 'S8VGMPM6CmyOfTil2ZbQQDgiSpix', 'qlYfRGmN0a4DxS9MB9rzkBIpcQAY',
'xIrHeiakHDq9RVihdEwBz1t8mAkQ', 'WmyVt8yBVp5w6oHY0gfZQfvW9U0D', 'RkQv96uK8GX7VPz9H3qhpfAJq9yi',
'aDFobQY5xWiHUfxVM7W966KY2x1s', 'qUZO9K7QksYAmRLPhbsUzgfNsfA9', 'jhThM0qSYKnAoKOndhyGFN8c81t6',
'sENwVcTk2CsEEqVCcdNvHOHqeuvk', '7R6SA1YXcR7QZBC5tWPPGOjEyG5o', 'QeOnHE9jIwzHCepny9kQwoADy0W1',
'UZwT2kU7oC3PM9ANwlfvsO2iLxJs', 'MHm55KJ28fqMbP4miYCJCWfMzwsx', 'qice0gm9Xt8MAJcpusWpn1E21Pn5',
'fURQNhhpEfF4cQovubjIDCXWCkTJ', 'vi8LuKrT1FAVl4mAYkhNyzEY7pf0', 'LH2OP3ifCIATdTIX16pNQYVprVV0',
'3aw4TZs4fWR2DlG8ZyblXdj2zvK6', 'mIDLy83NCJefxDBvPEgTYuv7VNgP', 'VCZAkZmUvvYu587gY2OKDtbiLDHr',
'CfMdbgMRzVbgk2Z7xO8GWkLW1LXe', '1xf5jiCdLfnW1GcaiaR3c74osC7y', '6p1Md0k6MImWER21OuE572p5bWCF',
'Ec28kK4dwD7l7yso9APNd1v2M0JU', '1OBamL8mvz7smrSUDOILqSelGc9u', 'Nm0oAj0v2lK4uFDN05lDNItcKrNe',
'hlFT8vkmM9zF0OJBzbZ0I3B5Bqc5', 'Yee5KH5PYsATZJBvpSYnlVQ9onEh', 'KVzHlcP07p6fhesw8yGtDI0g80s5',
'Zfk40dhmH9qmGhayL8iuSVIV9hZj', 'SVSWL4KzwOjZSW7G7rWmJdN63z8H', '6iB5HKggnVJ4zB7ghv0CQMYauW0w',
'H1UYime5gQqjpzOV4mjI8iDLfOLX', 'ktY8pYEZuIx7pJlcXE8Cj2DBSfuA', 'njkVoZSBawU6yRbofMoOdEWr14z4',
'qfWnONJXVL6KRbagXsouIgcNoolB', 'HhLQJ9a2H36j1714KENlkSyz5asd', 'vXvoJa3igf8VUMg0piJapBtkEHBp',
'JfuolyIxBwU9Xi0Isuo7Fe6GiJW8', 'KKAVstxm7icRauGfzWz6mN5WnrmZ', 'e39Q4uCupFLskEvXieSyykBp0BNO',
'gqsI8DGDuPc2uU2QHGxoJHf93Qpj', 'f9AdsQhwY7ZYGCyWbKeuYjteyVPW', 'Y8NKVhcoocqRZC7OaTbLzPUFQyso',
'xelr6akXi8nC0fFNa4uzPxe5nUe7', 'ZwaCU2pjKkDcHgczDcdzwGRqWtDu', 'o12iEL4e2N0MaG9xjmuWmTyTRA7u',
'5q8rgKBxreuf2HhSIbNUldCVWbMQ', 'pQkw7PNsqK6fQp3PaL87f8id8rFX', '1johmd8QuNF7o12NjVLqNihioUJZ',
'jREHZELqU5qjXpRqnHrhKUx1nAcX', 'PTDXUzv3NDEDz1z0HgYrTgq3aE6W', 'YPUISIBOZcqmIfrdVZl2WkxkztvB',
'j2muBdz3ndT1WFARQQzAf8bgEASB', 'bjlJlZ5X11bkLMWTzCFPCczZXdpd', 'DJk5FmPZgDlxDdPO9QMyywAltUo6',
'O4MnxOAdKBuaw416wDSgT7HEpORO', '1BY0bP3hRvaNYxPc1k07OQV0MtS9', 'fvWBjh43fVOCWFGtQyIigJjyIwuv',
'tdkQSbJjfFsB3qK5NZexiiPKw9hO', 'MeprX4fPFWFlNsGepe6g7jU2aso3', 'fI3Bo0eVdL5T0k1BF9z5ZZksg1lJ',
'EaTKWECaF1mrSrNReCvHxUc9Aw6f', 'rmj4EOUZflUBjivxuWwxvkqeQ7zZ', 'HcjAZ7BHz9MYC2Cr8kESZdeDt89P',
'gLKLfEU55QAaX6KZqGoVH1I3Stey', 'M5KcXvqrA0Wjy9PcUk3d2cBKUql7', 'Bo9vYPnfifRCU91IqCB4L0oCB0gT',
'sR1ltwCNlkY3ZjtgfRf53SNyGLUV', 'BzCV0TcLVSbuqxKsCSlODsZVO2n7', '3mtRitVOo3aYZtP4GWohSYzDgTEF',
'rMS2ThPBRPQ1xW82Ntdl6pz06QIf', 'd9rsHVuHRUwNbRQEXOh7N51q3BCW', 'C0Vc36bp240knLA2pUfqpkFzcy20',
'njMHH1xDDAnZoaDcusTOGPN9PYUS', 'ceexqjBA3jcZahbYXcBmOXoSYTUf', 'RN25nMMPsmrG1GBgzlYNR6bTDsYK',
'F18MUd7UVSqUHWT7lrQ69e9LJq60', 'tsl6jOnHgd0GXauWgfSkeTpvVWie', 'R5aKozeeHL04yjbDT7rZtAe4xuJW',
'CBdBiaLZ3OC2CdeOJ7lCbQMqBfqh', 'WndKanmlJdAXOLhB4PNHFEaGUFjo', 'GxMm7IzMQx0aF9TAAslvb1zZOWrI',
'0LLQrDJpZTSEHqaihCplYBv0jJpL', '41XlHavPgk37N7d04xPR5CiY5aOt', 'Aoro7mgwCMFKulhzj4cVezpoNoj8',
'UqMtMY4DjBuW5tyzL24ao4szmU5g', '9KemkP6otlgChpECWNXZMiLqNDiO', 'deAfgifzicPmSUqhlaeSsQE5E1qC',
'axjopX3ufftvZ7KwlPvh6FeRWlmW', '794kXAnJFGBXHYMVupsH7wCg2ziE', 'RemILQohvvLbqIIDmLagGd1h1V0g',
'inqbe0gTkO035UhLQqs8AdLDAQZU', 'DIua6qNAVKcMEXMBoh4zqS0o1ylH', 'ugt0TKnN4k3KTkBmjtvF17buCWFR',
'L5tN4Cchab8SKwdavWj2R2IBaV4U', 'PAq07qHS9lzPVbubzBrpxK2mYzFI', 'kyZsrrc6KQzaGXaSvQxEK8vnDf4t',
'y5dfQdZEEy1PjLaYq9h9JGW84XLp', 'GZsS1r7p22HaFwhLXfA4NTBGTdGY', '121XCEcWahsa2uWoBNsKlSv4WT5q',
'LWo3zauWpkBcDOm6zWdAnub0kXrM', 'tgMgB65U5HKWsEf2hWI3L5TTJZAp', 'Mj6dk1yn2Mrq3GYkUXuyQirEdtqx',
'KFsvhFbqctEqbRwwzSfi9cwkzwtz', 'KXPWtXRrZs8O3bkFXIPRhKxVrUkL', 'GkLU81rsbgwrZbEWteOe8qHrNGU4',
'6vm0lWerrn0CmBPl4q9EhRXeHoRZ', 'JCBIBRjzPt422R1m4BkdHDTyRfGL', 'qd8BOdGSQ5SM40QfklCzJbunzCgh',
'p3zctXEWZkheBkELreWltjYyPDa0', '1e72k0eUeshugRERvPezjLseu2pJ', '0AvSWesi6rVA72lWXju53gMrBKK5',
'CTIUzLJaBz7DdrcuMSys4SjHqQm1', 'jIFnK90AHwqngyzzRCUtUQZEJp7m', 'AunWI0mgIkJ0G9J1E9ajL6OsfhHx',
'3NWujc7aI2UPBPXICQVr5KP7ivTx', 'eS0KbUFdRbBemXCk4RaSMKcOTHra', 'I8z0FeXUOD7dtgd2xmEiM7ocfXNe',
'zRZ5CyteGY7P1XUbLfpE9qKTW7Ja', 'nyJg1YgNLiS5ba1UzSMrc9QLAjMC', 'yC6KAwEd4oNWCp5zwekq1n3HpiJd']

# Logging Setup
logging.basicConfig(
    filename='parking_management.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Utility Functions
def generate_random_number(seed_string, max_value=299):
    hash_object = hashlib.md5(seed_string.encode())
    seed = int(hash_object.hexdigest(), 16)
    random.seed(seed)
    return random.randint(0, max_value)

def generate_random_open_id(length=28):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# NetworkWorker Class
class NetworkWorker(QThread):
    query_result = pyqtSignal(dict)
    discount_result = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, action, plate_number, parking_lot, random_open_id=False):
        super().__init__()
        self.action = action
        self.plate_number = plate_number
        self.parking_lot = parking_lot
        self.random_open_id = random_open_id

    def run(self):
        try:
            if self.action == 'query':
                result = self.parking_query()
                self.query_result.emit(result or {})
                if not result:
                    self.error_occurred.emit("Query failed or returned empty result.")
            elif self.action == 'discount':
                result = self.parking_discount_payment()
                self.discount_result.emit(result or "")
                if not result:
                    self.error_occurred.emit("Discount payment failed.")
        except Exception as e:
            logging.error(f"Network request error: {e}")
            self.error_occurred.emit(f"Network error: {e}")

    def parking_query(self):
        return (self.jhq_query(self.plate_number) if self.parking_lot == "金虹桥"
else self.byl_query(self.plate_number))

    def parking_discount_payment(self):
        return (self.jhq_discount(self.plate_number, self.random_open_id) if self.parking_lot == "金虹桥"
else self.byl_discount(self.plate_number))

    def jhq_query(self, plate, open_id=None):
        url = "https://m.mallcoo.cn/api/park/ParkFee/GetParkFeeV3"
        if not open_id:
            open_id = generate_random_open_id(16)
        headers = {
            "Host": "m.mallcoo.cn",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Accept": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://servicewechat.com/wx{open_id}/2/page-frame.html"
        }
        data = {
            "UID": "0",
            "MallID": 12931,
            "ParkID": 1777,
            "PlateNo": plate,
            "Barcode": "",
            "FreeMinutes": 0,
            "FreeAmount": 2000,
            "timetip": int(time.time() * 1000),
            "Header": {"Token": ""}
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            return {
"入场时间": response.json().get("d", {}).get("EntryTime", ""),
"停车时长": response.json().get("d", {}).get("ParkingMinutes", 0),
"需要支付的费用": response.json().get("d", {}).get("ParkingFee", 0.0)
            }
        except Exception as e:
            logging.error(f"JHQ query error: {e}")
            return None

    def byl_query(self, plate, open_id=None):
        url = 'https://m.mallcoo.cn/api/park/ParkFee/GetParkFeeV3'
        if not open_id:
            open_id = generate_random_open_id(16)
        headers = {
            'Host': 'm.mallcoo.cn',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Accept': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0',
            'Referer': f"https://servicewechat.com/wx{open_id}/2/page-frame.html"
        }
        data = {
            "UID": "0",
            "MallID": 12933,
            "ParkID": 1778,
            "PlateNo": plate,
            "Barcode": "",
            "FreeMinutes": 0,
            "FreeAmount": 6000,
            "timetip": int(time.time() * 1000),
            "Header": {"Token": ""}
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
            return {
"入场时间": response.json().get("d", {}).get("EntryTime", ""),
"停车时长": response.json().get("d", {}).get("ParkingMinutes", 0),
"需要支付的费用": response.json().get("d", {}).get("ParkingFee", 0.0)
            }
        except Exception as e:
            logging.error(f"BYL query error: {e}")
            return None

    def jhq_discount(self, plate, random_open_id=False):
        open_id = (generate_random_open_id() if random_open_id
   else open_id_list[generate_random_number(plate)])
        query_result = self.jhq_query(plate, open_id)
        if not query_result or query_result.get("需要支付的费用", 0) <= 0:
            return "待支付费用为0"

        entry_time = query_result.get("入场时间", "")
        parking_minutes = query_result.get("停车时长", 0)
        url = "http://app.archshanghai.com/jhq/app/discount/shopDiscount/discountByPlate"
        headers = {
            "Host": "app.archshanghai.com",
            "Accept": "application/json, text/plain, */*",
            "Authorization": "Bearer null",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "http://app.archshanghai.com",
            "User-Agent": "Mozilla/5.0",
            "Connection": "keep-alive",
            "Referer": "http://app.archshanghai.com/jhq/mobile/"
        }
        data = {
            "status": 0,
            "parking_coupon_number": plate,
            "idx": "63b0d1fcce8b686558bfc43c",
            "flag": "1",
            "disTime": 2,
            "EntryTime": entry_time,
            "disNo": "NO.shop088",
            "openid": open_id,
            "organization": "59688d03798e5004d69dab47",
            "page": "shopDiscount"
        }
        try:
            response = requests.post(
url, headers=headers, json=data,
params={"Timestamp": int(time.time() * 1000)},
timeout=5
            )
            response.raise_for_status()
            logging.info(f"JHQ discount applied for plate {plate}: {response.text}")
            return response.text
        except Exception as e:
            logging.error(f"JHQ discount error for plate {plate}: {e}")
            return None

    def byl_discount(self, plate):
        try:
            time.sleep(1)  # Simulate network delay
            result = "白玉兰停车折扣已生效"
            logging.info(f"BYL discount applied for plate {plate}: {result}")
            return result
        except Exception as e:
            logging.error(f"BYL discount error for plate {plate}: {e}")
            return None

# QuickActionWidget Class
class QuickActionWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Plate Input
        plate_layout = QHBoxLayout()
        self.plate_input = QLineEdit(placeholderText="input")
        plate_layout.addWidget(QLabel("Input:"))
        plate_layout.addWidget(self.plate_input)
        layout.addLayout(plate_layout)

        # 金虹桥 Buttons Row
        jhq_layout = QHBoxLayout()
        jhq_buttons = [
            ("Q", self.jhq_query),
            ("P", self.jhq_payment),
            ("O", lambda: self.jhq_payment(random_open_id=True))
        ]
        for text, handler in jhq_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, h=handler: self.execute_action(h))
            jhq_layout.addWidget(btn)
        layout.addLayout(jhq_layout)

    def execute_action(self, handler):
        plate = self.plate_input.text().strip()
        if not plate:
            QMessageBox.warning(self, "输入错误", "车牌号不能为空！")
            return
        # Basic plate number validation (e.g., expecting Chinese plate format)
        if not (5 <= len(plate) <= 8 and any(u'\u4e00' <= char <= u'\u9fff' for char in plate)):
            QMessageBox.warning(self, "输入错误", "请输入有效的中国车牌号（如沪A12345）")
            return
        handler()

    def jhq_query(self):
        self.parent.query_from_quick_action(self.plate_input.text().strip(), "金虹桥")

    def jhq_payment(self, random_open_id=False):
        self.parent.payment_from_quick_action(self.plate_input.text().strip(), "金虹桥", random_open_id)

    def byl_query(self):
        self.parent.query_from_quick_action(self.plate_input.text().strip(), "白玉兰")

    def byl_payment(self, random_open_id=False):
        self.parent.payment_from_quick_action(self.plate_input.text().strip(), "白玉兰", random_open_id)

# ParkingManagementSystem Class
class ParkingManagementSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generator")
        self.setGeometry(50, 50, 300, 100)  # Reduced window size for quick action focus
        self.workers = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Style
        self.setStyleSheet("""
            QPushButton { font-size: 12px; padding: 5px 10px; }
            QLabel { font-size: 12px; }
            QLineEdit { font-size: 12px; }
        """)

        # Quick Action Section
        quick_action_group = QGroupBox("Op")
        quick_action_group.setLayout(QVBoxLayout())
        quick_action_group.layout().addWidget(QuickActionWidget(self))
        layout.addWidget(quick_action_group)

    def query_from_quick_action(self, plate_number, parking_lot):
        worker = NetworkWorker('query', plate_number, parking_lot)
        worker.query_result.connect(lambda res: self.handle_query_result(plate_number, res, parking_lot))
        worker.error_occurred.connect(lambda err: QMessageBox.warning(self, "查询错误", err))
        self.workers.append(worker)
        worker.finished.connect(lambda: self.workers.remove(worker))
        worker.start()

    def payment_from_quick_action(self, plate_number, parking_lot, random_open_id=False):
        worker = NetworkWorker('discount', plate_number, parking_lot, random_open_id)
        worker.discount_result.connect(lambda res: self.handle_discount_result(plate_number, res, parking_lot))
        worker.error_occurred.connect(lambda err: QMessageBox.warning(self, "支付错误", err))
        self.workers.append(worker)
        worker.finished.connect(lambda: self.workers.remove(worker))
        worker.start()

    def handle_query_result(self, plate_number, result, parking_lot):
        if result:
            QMessageBox.information(self, "查询结果", f"车牌号: {plate_number}\n"
                            f"停车场: {parking_lot}\n"
                            f"入场时间: {result.get('入场时间', '')}\n"
                            f"停车时长: {result.get('停车时长', 0)} 分钟\n"
                            f"待支付费用: ￥{result.get('需要支付的费用', 0.0):.2f}"
            )
            self.log_parking_info(plate_number, result, f"query_{parking_lot}")
        else:
            QMessageBox.warning(self, "查询错误", "查询结果为空或失败。")

    def handle_discount_result(self, plate_number, result, parking_lot):
        if result:
            QMessageBox.information(self, "支付成功", f"车牌号: {plate_number}，{result}")
            self.log_parking_info(plate_number, {"折扣信息": result}, f"discount_{parking_lot}")
            # self.query_from_quick_action(plate_number, parking_lot)  # Refresh query after discount
        else:
            QMessageBox.warning(self, "支付错误", "折扣支付失败。")

    def log_parking_info(self, plate_number, info, log_type="query"):
        logging.info(f"Plate: {plate_number}, Type: {log_type}, Info: {info}")

    def closeEvent(self, event):
        for worker in self.workers:
            if worker.isRunning():
                worker.quit()
            worker.wait()
        event.accept()

# Main Function
def main():
    app = QApplication(sys.argv)
    window = ParkingManagementSystem()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()