from flask import jsonify, make_response, request
from data import session
import flask
from data.jobs import Jobs

jobs_blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@jobs_blueprint.route('/api/jobs')
def get_jobs():
    db_sess = session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'news':
                [item.to_dict() for item in jobs]
        }
    )
