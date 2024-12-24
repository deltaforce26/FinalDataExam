import os
from datetime import datetime

from flask import Blueprint, jsonify, request, send_from_directory, Response
from app.db.mongo_db import initialize_mongo
from app.repositories.attacks_repo import get_all_documents
from app.repositories.stat_repo import find_most_fatal_attacks, find_most_violent_groups, find_top_groups_per_country, \
    find_common_targets
from app.services.graph_service import create_common_targets_graph
from app.services.map_service import create_avg_map, create_most_active_group_map, create_geo_heat_map
from app.settings.config import DB_URL

stat_bp = Blueprint('stat_bp', __name__)


@stat_bp.route('/most_fatal_attack_type', methods=["GET"])
def get_most_fatal_attack_type():
    limit = request.args.get('limit')
    if limit is None:
        attack_types = find_most_fatal_attacks()
    else:
        attack_types = find_most_fatal_attacks(int(limit))
    return jsonify({"Attack types": attack_types}), 200



@stat_bp.route('/casualties_avg', methods=["GET"])
def get_casualties_avg():
    limit = request.args.get('limit')
    if limit is None:
        map_path = create_avg_map()
    else:
        map_path = create_avg_map(int(limit))
    maps_dir = os.path.dirname(map_path)
    map_filename = os.path.basename(map_path)
    return send_from_directory(maps_dir, map_filename)



@stat_bp.route('/most_violent_groups', methods=["GET"])
def get_most_violent_groups():
    limit = request.args.get('limit')
    if limit is None:
        most_violent_groups = find_most_violent_groups()
    else:
        most_violent_groups = find_most_violent_groups(int(limit))
    return jsonify({"Violent groups": most_violent_groups}), 200


@stat_bp.route('/most_active_group', methods=["GET"])
def get_most_active_group():
    country = request.args.get('country')
    if country is None:
        most_active_group = find_top_groups_per_country()
    else:
        most_active_group = find_top_groups_per_country(country)
    groups_map_path = create_most_active_group_map(most_active_group)
    maps_dir = os.path.dirname(groups_map_path)
    map_filename = os.path.basename(groups_map_path)
    return send_from_directory(maps_dir, map_filename)


@stat_bp.route('/geo_heat_map', methods=["GET"])
def get_heat_map():
    attacks_col = initialize_mongo(DB_URL, "terror_attacks_db", "attacks")
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            docs = get_all_documents(attacks_col, start_date, end_date)
        except ValueError as e:
            print(f'Invalid date format: {e}')
    else:
        docs = get_all_documents(attacks_col)
    geo_heat_map_path = create_geo_heat_map(docs)
    maps_dir = os.path.dirname(geo_heat_map_path)
    map_filename = os.path.basename(geo_heat_map_path)
    return send_from_directory(maps_dir, map_filename)


@stat_bp.route('/common_targets', methods=["GET"])
def get_common_targets():
    common_targets = find_common_targets()
    print(f"Common targets: {common_targets}")
    graph = create_common_targets_graph(common_targets)
    return Response(graph, mimetype='image/png')