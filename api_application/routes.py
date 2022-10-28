from api_application import api, db
from flask_restful import reqparse, abort, Resource
from flask import request
from api_application.models import ResultsModel
from datetime import datetime as dt


records_post_args = reqparse.RequestParser()
records_post_args.add_argument('type')
records_post_args.add_argument('operator')
records_post_args.add_argument('datetime')
records_post_args.add_argument('result')


def abort_if_record_id_doesnt_exist(record_id):
    if not ResultsModel.query.filter_by(id=record_id).first():
        abort(409, message="Could not find record")


def statistic(result):
    res_dict = {}
    for res in result:
        if res.type not in res_dict:
            if res.result == 1:
                res_dict[res.type] = {"total": 1, "true": 1, "false": 0}
            else:
                res_dict[res.type] = {"total": 1, "true": 0, "false": 1}
        else:
            res_dict[res.type]["total"] += 1
            if res.result == 1:
                res_dict[res.type]["true"] += 1
            else:
                res_dict[res.type]["false"] += 1
    return res_dict


class Result(Resource):
    def get(self):
        if request.args.get('operator'):
            result = ResultsModel.query.filter_by(operator=str(request.args.get('operator')))
            return statistic(result), 200
        else:
            result = ResultsModel.query.all()
            return statistic(result), 200


class ResultAdd(Resource):
    def post(self):
        data = records_post_args.parse_args()
        data['type'] = str(data['type'])
        data['operator'] = str(data['operator'])
        data['datetime'] = str(dt.strptime(data['datetime'], "%Y-%m-%d %H:%M:%S"))
        data['result'] = int(data["result"])
        new_data = ResultsModel(**data)
        db.session.add(new_data)
        db.session.commit()
        return data, 201


class ResultDel(Resource):
    def delete(self, record_id):
        abort_if_record_id_doesnt_exist(record_id)
        # record = ResultsModel.query.filter_by(id=record_id).first()
        record = ResultsModel.query.get(record_id)
        db.session.delete(record)
        db.session.commit()
        return {"message": f'Record {record_id} is successfully deleted'}, 200


api.add_resource(Result, "/api_v1/stat/")  # отримання статистики з опціональним фільтром
api.add_resource(ResultAdd, "/api_v1/test_result")  # додавання нового результату тесту в БД
api.add_resource(ResultDel, "/api_v1/test_result/<int:record_id>")  # видалення запису по id