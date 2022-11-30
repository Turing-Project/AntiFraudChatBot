## Generated Story No1
* greet
    - utter_greet
* deny
    - utter_goodbye

## Generated Story No2
* greet
    - utter_greet
* goodbye
    - utter_goodbye

## Generated Story No3
* greet
    - utter_greet
* thanks
    - utter_thanks

## Generated Story No4
* unknown_intent
  - action_default_fallback

## Generated Story No5
* greet
    - utter_greet
* request_search{"item": "\u8bdd\u8d39"}
    - slot{"item": "\u8bdd\u8d39"}
    - utter_ask_time
* inform{"time": "\u4e09\u6708"}
    - slot{"time": "\u4e09\u6708"}
    - utter_confirm
* confirm
    - action_search_consume
    - utter_ask_morehelp
* deny
    - utter_goodbye


## Generated Story No6
* greet
    - utter_greet
* request_search{"item": "\u6d41\u91cf", "time": "\u4e09\u6708"}
    - slot{"item": "\u6d41\u91cf"}
    - slot{"time": "\u4e09\u6708"}
    - utter_confirm
* confirm
    - action_search_consume
    - utter_ask_morehelp
* deny
    - utter_goodbye


## Generated Story No7
* greet
    - utter_greet
* request_management{"package": "\u5957\u9910"}
    - slot{"package": "\u5957\u9910"}
    - utter_ask_package
* inform{"package": "\u5957\u9910\u4e00"}
    - slot{"package": "\u5957\u9910\u4e00"}
    - utter_confirm
* confirm
    - utter_ack_management
    - utter_ask_morehelp
* deny
    - utter_goodbye
* thanks
    - utter_thanks

## Generated Story No8
* greet
    - utter_greet
* request_management{"package": "\u5957\u9910"}
    - slot{"package": "\u5957\u9910"}
    - utter_ask_package
* inform{"package": "\u5957\u9910\u4e00"}
    - slot{"package": "\u5957\u9910\u4e00"}
    - utter_confirm
* confirm
    - utter_ack_management
    - utter_ask_morehelp
* request_search{"item": "\u6d41\u91cf", "time": "\u4e09\u6708"}
    - slot{"item": "\u6d41\u91cf"}
    - slot{"time": "\u4e09\u6708"}
    - utter_confirm
* confirm
    - action_search_consume
    - utter_ask_morehelp
* deny
    - utter_goodbye

## Generated Story No9
* greet
    - utter_greet
* request_management{"package": "\u5957\u9910"}
    - slot{"package": "\u5957\u9910"}
    - utter_ask_package
* request_search{"item": "\u6d41\u91cf", "time": "\u4e09\u6708"}
    - slot{"item": "\u6d41\u91cf"}
    - slot{"time": "\u4e09\u6708"}
    - utter_confirm
* confirm
    - action_search_consume
    - utter_ask_morehelp
* deny
    - utter_goodbye

## Generated Story No10
* greet
    - utter_greet
* request_management{"package": "\u5957\u9910"}
    - slot{"package": "\u5957\u9910"}
    - utter_ask_package
* request_search{"item": "\u6d41\u91cf"}
    - slot{"item": "\u6d41\u91cf"}
    - utter_ask_time
* inform{"time": "\u4e09\u6708"}
    - slot{"time": "\u4e09\u6708"}
    - utter_confirm
* confirm
    - action_search_consume
    - utter_ask_morehelp
* deny
    - utter_goodbye