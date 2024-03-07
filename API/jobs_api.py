from flask import jsonify, make_response, request
from data import session
import flask
from data.jobs import Jobs

jobs_blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@jobs_blueprint.route('/api/jobs')
def get_jobs():
    db_sess = session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict() for item in jobs]
        }
    )


@jobs_blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs': jobs.to_dict()
        }
    )


@jobs_blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = session.create_session()

    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['bob'],
        content=request.json['content'],
        work_size=request.json['work_size'],
        colloboration=request.json['colloboration'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})
