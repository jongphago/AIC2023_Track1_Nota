import numpy as np
from pathlib import Path
import cv2
import os
import pickle
import json


_COLORS = np.array(
    [
        0.000, 0.447, 0.741,
        0.850, 0.325, 0.098,
        0.929, 0.694, 0.125,
        0.494, 0.184, 0.556,
        0.466, 0.674, 0.188,
        0.301, 0.745, 0.933,
        0.635, 0.078, 0.184,
        0.300, 0.300, 0.300,
        0.600, 0.600, 0.600,
        1.000, 0.000, 0.000,
        1.000, 0.500, 0.000,
        0.749, 0.749, 0.000,
        0.000, 1.000, 0.000,
        0.000, 0.000, 1.000,
        0.667, 0.000, 1.000,
        0.333, 0.333, 0.000,
        0.333, 0.667, 0.000,
        0.333, 1.000, 0.000,
        0.667, 0.333, 0.000,
        0.667, 0.667, 0.000,
        0.667, 1.000, 0.000,
        1.000, 0.333, 0.000,
        1.000, 0.667, 0.000,
        1.000, 1.000, 0.000,
        0.000, 0.333, 0.500,
        0.000, 0.667, 0.500,
        0.000, 1.000, 0.500,
        0.333, 0.000, 0.500,
        0.333, 0.333, 0.500,
        0.333, 0.667, 0.500,
        0.333, 1.000, 0.500,
        0.667, 0.000, 0.500,
        0.667, 0.333, 0.500,
        0.667, 0.667, 0.500,
        0.667, 1.000, 0.500,
        1.000, 0.000, 0.500,
        1.000, 0.333, 0.500,
        1.000, 0.667, 0.500,
        1.000, 1.000, 0.500,
        0.000, 0.333, 1.000,
        0.000, 0.667, 1.000,
        0.000, 1.000, 1.000,
        0.333, 0.000, 1.000,
        0.333, 0.333, 1.000,
        0.333, 0.667, 1.000,
        0.333, 1.000, 1.000,
        0.667, 0.000, 1.000,
        0.667, 0.333, 1.000,
        0.667, 0.667, 1.000,
        0.667, 1.000, 1.000,
        1.000, 0.000, 1.000,
        1.000, 0.333, 1.000,
        1.000, 0.667, 1.000,
        0.333, 0.000, 0.000,
        0.500, 0.000, 0.000,
        0.667, 0.000, 0.000,
        0.833, 0.000, 0.000,
        1.000, 0.000, 0.000,
        0.000, 0.167, 0.000,
        0.000, 0.333, 0.000,
        0.000, 0.500, 0.000,
        0.000, 0.667, 0.000,
        0.000, 0.833, 0.000,
        0.000, 1.000, 0.000,
        0.000, 0.000, 0.167,
        0.000, 0.000, 0.333,
        0.000, 0.000, 0.500,
        0.000, 0.000, 0.667,
        0.000, 0.000, 0.833,
        0.000, 0.000, 1.000,
        0.000, 0.000, 0.000,
        0.143, 0.143, 0.143,
        0.286, 0.286, 0.286,
        0.429, 0.429, 0.429,
        0.571, 0.571, 0.571,
        0.714, 0.714, 0.714,
        0.857, 0.857, 0.857,
        0.000, 0.447, 0.741,
        0.314, 0.717, 0.741,
        0.50, 0.5, 0
    ]
).astype(np.float32).reshape(-1, 3)

sources = {
        # AIHUB
        'AV019': [f'./datasets/AV019/c0{i:02d}/' for i in range(1, 17)],
        # Test
        'S001': [
                './datasets/S001/c001/',
                './datasets/S001/c002/',
                './datasets/S001/c003/',
                './datasets/S001/c004/',
                './datasets/S001/c005/',
                './datasets/S001/c006/',
                './datasets/S001/c007/',
                ],
        'S003': [
                './datasets/S003/c014/',
                './datasets/S003/c015/',
                './datasets/S003/c016/',
                './datasets/S003/c017/',
                './datasets/S003/c018/',
                './datasets/S003/c019/',
                ],
        'S009': [
                './datasets/S009/c047/',
                './datasets/S009/c048/',
                './datasets/S009/c049/',
                './datasets/S009/c050/',
                './datasets/S009/c051/',
                './datasets/S009/c052/',
                ],
        'S014': [
                './datasets/S014/c076/',
                './datasets/S014/c077/',
                './datasets/S014/c078/',
                './datasets/S014/c079/',
                './datasets/S014/c080/',
                './datasets/S014/c081/',
                ],
        'S018': [
                './datasets/S018/c100/',
                './datasets/S018/c101/',
                './datasets/S018/c102/',
                './datasets/S018/c103/',
                './datasets/S018/c104/',
                './datasets/S018/c105/',
                ],
        'S021': [
                './datasets/S021/c118/',
                './datasets/S021/c119/',
                './datasets/S021/c120/',
                './datasets/S021/c121/',
                './datasets/S021/c122/',
                './datasets/S021/c123/',
                ],
        'S022': [
                './datasets/S022/c124/',
                './datasets/S022/c125/',
                './datasets/S022/c126/',
                './datasets/S022/c127/',
                './datasets/S022/c128/',
                './datasets/S022/c129/',
                ],
        }

result_paths = {
    # AIHUB
    'AV019': './results/AV019.txt',
    # Test
    'S001': './results/S001.txt',
    'S003': './results/S003.txt',
    'S009': './results/S009.txt',
    'S014': './results/S014.txt',
    'S018': './results/S018.txt',
    'S021': './results/S021.txt',
    'S022': './results/S022.txt',
    }

map_infos = {
    "AV019": {
        "size" : (1591,896),
        "source" : "./datasets/AV019/map.png",
        "savedir" : "./output_videos/mapAV019.mp4"
    },
    # Test
    "S001": {
        "size" : (1591,896),
        "source" : "./datasets/S001/map.png",
        "savedir" : "./output_videos/mapS001.mp4"
    },
    "S003": {
        "size" : (1777,784),
        "source" : "./datasets/S003/map.png",
        "savedir" : "./output_videos/mapS003.mp4"
    },
    "S009": {
        "size" : (1534,1398),
        "source" : "./datasets/S009/map.png",
        "savedir" : "./output_videos/mapS009.mp4"
    },
    "S014": {
        "size" : (1889,1322),
        "source" : "./datasets/S014/map.png",
        "savedir" : "./output_videos/mapS014.mp4"
    },
    "S018": {
        "size" : (969,1036),
        "source" : "./datasets/S018/map.png",
        "savedir" : "./output_videos/mapS018.mp4"
    },
    "S021": {
        "size" : (1898,889),
        "source" : "./datasets/S021/map.png",
        "savedir" : "./output_videos/mapS021.mp4"
    },
    "S022": {
        "size" : (1903,905),
        "source" : "./datasets/S022/map.png",
        "savedir" : "./output_videos/mapS022.mp4"
    },
    }

cam_ids = {
    "AV019": [str(i) for i in range(1, 17)],
    # Test
    'S001': ['1', '2', '3', '4', '5', '6', '7'],
    'S003': ['14', '15', '16', '17', '18', '19'],
    'S009': ['47', '48', '49', '50', '51', '52'],
    'S014': ['76', '77', '78', '79', '80', '81'],
    'S018': ['100', '101', '102', '103', '104', '105'],
    'S021': ['118', '119', '120', '121', '122', '123'],
    'S022': ['124', '125', '126', '127', '128', '129'],
}

def get_reader_writer(source):
    src_paths = sorted([p for p in os.listdir(source) if (p != "video.mp4")],  key=lambda x: int(x.split("_")[-1].split(".")[0]))
    src_paths = [os.path.join(source, s) for s in src_paths]

    fps = 30
    wi, he = 1920, 1080
    # dst = 'output_videos/' + source.replace('/','').replace('.','') + '.mp4'
    dst = 'output_videos/' + source.split('/')[-3] + source.split('/')[-2] + '.mp4'
    video_writer = cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*'mp4v'), fps, (wi, he))

    print(f"{source}'s total frames: {len(src_paths)}")
    
    return [src_paths, video_writer]

def finalize_cams(src_handlers):
    for s, w in src_handlers:
        w.release()
        print(f"{w} released")

def write_vids(trackers, imgs, src_handlers, latency, pose, colors, mc_tracker, cur_frame=0):

    writers = [w for s, w in src_handlers]
    gid_2_lenfeats = {}
    for track in mc_tracker.tracked_mtracks + mc_tracker.lost_mtracks:
        if track.is_activated:
            gid_2_lenfeats[track.track_id] = len(track.features)
        else:
            gid_2_lenfeats[-2] = len(track.features)

    for tracker, img, w in zip(trackers, imgs, writers):
        outputs = [t.tlbr.tolist() + [t.score, t.global_id, gid_2_lenfeats.get(t.global_id, -1)] for t in tracker.tracked_stracks]
        pose_result = [t.pose for t in tracker.tracked_stracks if t.pose is not None]
        img = visualize(outputs, img, latency, colors, pose, pose_result, cur_frame)
        w.write(img)

def write_det_vids(dets, imgs, src_handlers, latency, colors, cur_frame):
    writers = [w for s, w in src_handlers]
    for det, img, w in zip(dets, imgs, writers):
        img = visualize_det(det, img, latency, colors, cur_frame)
        w.write(img)

def write_results(result_lists, result_paths):
    single_folder = str(Path(result_paths[0][0]).parent)
    multi_folder = str(Path(result_paths[1][0]).parent)
    os.makedirs(single_folder, exist_ok=True)
    os.makedirs(multi_folder, exist_ok=True)
    # write singlecam results
    for result, path in zip(result_lists, result_paths[0]):
        print(path)
        with open(path, 'w') as f:
            for r in result:
                f.write(r)
    # write multicam results
    with open(result_paths[1][0], 'w') as f:
        print(result_paths[1][0])
        for i, result in enumerate(result_lists):
            for r in result:
                r = r.split(" ")
                r[0] = str(int(r[0]) + 18010*i)
                r = " ".join(r)
                f.write(r)

def write_results_testset(result_lists, result_path):
    dst_folder = str(Path(result_path).parent)
    os.makedirs(dst_folder, exist_ok=True)
    # write multicam results
    with open(result_path, 'w') as f:
        print(result_path)
        for result in result_lists:
            for r in result:
                t, l, w, h = r['tlwh']
                xworld, yworld = r['2d_coord']
                row = [r['cam_id'], r['track_id'], r['frame_id'], int(t), int(l), int(w), int(h), int(xworld), int(yworld)]
                row = " ".join([str(r) for r in row]) + '\n'
                # row = " ".join(row)
                f.write(row)

def update_result_lists(trackers, result_lists, frame_id):
    if frame_id in (1,18010):  # matches the number of frames in the gt file
        return
    for tracker, result_list in zip(trackers, result_lists):
        outputs = [t.tlwh.tolist() + [t.global_id, t.score] for t in tracker.tracked_stracks if t.global_id < 0]
        for out in outputs:
            bb_left, bb_top, bb_width, bb_height, track_id, conf = out
            # it would be beneficial to include x,y if possible when submit result on evaluation server
            result = [frame_id, track_id, round(bb_left,3), round(bb_top,3), round(bb_width,3), round(bb_height,3), round(conf,3), -1, -1, -1]
            result = " ".join([str(r) for r in result]) + '\n'
            result_list.append(result)

def update_result_lists_testset(trackers, result_lists, frame_id, cam_ids, scene):
    results_frame = [[] for i in range(len(result_lists))]
    results_frame_feat = []
    for tracker, result_frame, result_list, cam_id in zip(trackers, results_frame, result_lists, cam_ids):
        for track in tracker.tracked_stracks:
            if track.global_id < 0: continue
            result = {
                'cam_id': int(cam_id),
                'frame_id': frame_id,
                'track_id': track.global_id,
                'sct_track_id': track.track_id,
                'tlwh': list(map(lambda x: int(x), track.tlwh.tolist())),
                # 'conf': track.score,
                '2d_coord': track.location[0].tolist(),
                # 'feat': track.curr_feat.tolist()
            }
            result_ = list(result.values())
            result_list.append(result)
            result['feat']=track.curr_feat.tolist()
            results_frame_feat.append(result)
            result_frame.append([result_[0], result_[1], result_[2], result_[3], result_[4][0],
                                result_[4][1], result_[4][2], result_[4][3], result_[5][0], result_[5][1]])
    # with open(f'./before_offline/{scene}_x6/{frame_id}.json', 'w') as file:
    #     json.dump(results_frame_feat, file, indent='\t')
    # with open(f'./before_offline/{scene}_x6/{scene}.txt', 'a') as lf:
    #     for result in results_frame:
    #         for re in result:
    #             lf.write(f'{re[0]} {re[1]} {re[2]} {re[3]} {re[4]} {re[5]} {re[6]} {re[7]} {re[8]} {re[9]}\n')


def visualize_det(dets, img, latency, colors, cur_frame):
    m = 2
    if len(dets) == 0:
        font = cv2.FONT_HERSHEY_SIMPLEX
        # text = 'FPS : {0:0.1f}'.format(1/latency)
        text = 'Latency : {0:0.3f} ms / Frame : {1}'.format(latency*1000, cur_frame)
        txt_size = cv2.getTextSize(text, font, 0.4*m, 1*m)[0]
        cv2.rectangle(img, (0, 0), (txt_size[0], int(1.5*txt_size[1])), (0,0,0), -1)
        cv2.putText(img, text, (0,txt_size[1]), font, 0.4*m, (255,255,255), thickness=1*m)
        return img
    
    for obj in dets:
        score = obj[4]
        track_id = int(obj[5])
        # cls_id = int(obj[6])
        # len_feats = ' ' if obj[6] == 50 else obj[6]
        x0, y0, x1, y1 = int(obj[0]), int(obj[1]), int(obj[2]), int(obj[3])

        color = (colors[track_id%80] * 255).astype(np.uint8).tolist()
        text = '{} : {:.1f}%'.format(track_id, score * 100)
        txt_color = (0, 0, 0) if np.mean(colors[track_id%80]) > 0.5 else (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        txt_size = cv2.getTextSize(text, font, 0.4*m, 1*m)[0]
        cv2.rectangle(img, (x0, y0), (x1, y1), color, 2)

        txt_bk_color = (colors[track_id%80] * 255 * 0.7).astype(np.uint8).tolist()
        cv2.rectangle(
            img,
            (x0, y0 - 1),
            (x0 + txt_size[0] + 1, y0 - int(1.5*txt_size[1])),
            txt_bk_color,
            -1
        )
        cv2.putText(img, text, (x0, y0 - txt_size[1]), font, 0.4*m, txt_color, thickness=1*m)

    # text = 'FPS : {0:0.1f}'.format(1/latency)
    text = 'Latency : {0:0.3f} ms / Frame : {1}'.format(latency*1000, cur_frame)
    txt_size = cv2.getTextSize(text, font, 0.4*m, 1*m)[0]
    cv2.rectangle(img, (0, 0), (txt_size[0], int(1.5*txt_size[1])), (0,0,0), -1)
    cv2.putText(img, text, (0,txt_size[1]), font, 0.4*m, (255,255,255), thickness=1*m)
    
    return img


def visualize(dets, img, latency, colors, pose, pose_result, cur_frame):
    m = 2
    if len(dets) == 0:
        font = cv2.FONT_HERSHEY_SIMPLEX
        # text = 'FPS : {0:0.1f}'.format(1/latency)
        text = 'Latency : {0:0.3f} ms / Frame : {1}'.format(latency*1000, cur_frame)
        txt_size = cv2.getTextSize(text, font, 0.4*m, 1*m)[0]
        cv2.rectangle(img, (0, 0), (txt_size[0], int(1.5*txt_size[1])), (0,0,0), -1)
        cv2.putText(img, text, (0,txt_size[1]), font, 0.4*m, (255,255,255), thickness=1*m)
        return img
            
    for obj in dets:
        score = obj[4]
        track_id = int(obj[5])
        # cls_id = int(obj[6])
        len_feats = ' ' if obj[6] == 50 else obj[6]
        x0, y0, x1, y1 = int(obj[0]), int(obj[1]), int(obj[2]), int(obj[3])

        color = (colors[track_id%80] * 255).astype(np.uint8).tolist()
        text = '{} : {:.1f}% | {}'.format(track_id, score * 100, len_feats)
        txt_color = (0, 0, 0) if np.mean(colors[track_id%80]) > 0.5 else (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        txt_size = cv2.getTextSize(text, font, 0.4*m, 1*m)[0]
        cv2.rectangle(img, (x0, y0), (x1, y1), color, 2)

        txt_bk_color = (colors[track_id%80] * 255 * 0.7).astype(np.uint8).tolist()
        cv2.rectangle(
            img,
            (x0, y0 - 1),
            (x0 + txt_size[0] + 1, y0 - int(1.5*txt_size[1])),
            txt_bk_color,
            -1
        )
        cv2.putText(img, text, (x0, y0 - txt_size[1]), font, 0.4*m, txt_color, thickness=1*m)

    # text = 'FPS : {0:0.1f}'.format(1/latency)
    text = 'Latency : {0:0.3f} ms / Frame : {1}'.format(latency*1000, cur_frame)
    txt_size = cv2.getTextSize(text, font, 0.4*m, 1*m)[0]
    cv2.rectangle(img, (0, 0), (txt_size[0], int(1.5*txt_size[1])), (0,0,0), -1)
    cv2.putText(img, text, (0,txt_size[1]), font, 0.4*m, (255,255,255), thickness=1*m)
    
    return img

def write_map(trackers, img, writer, colors, mc_tracker, cur_frame=0):
    gid_2_lenfeats = {}
    for track in mc_tracker.tracked_mtracks + mc_tracker.lost_mtracks:
        if track.is_activated:
            gid_2_lenfeats[track.track_id] = len(track.features)
        else:
            gid_2_lenfeats[-2] = len(track.features)

    origin_img = img.copy()
    for cam_id, tracker in enumerate(trackers):
        for track in tracker.tracked_stracks:
            loc = track.location[0]
            loc = [int(loc[0]), int(loc[1])]
            track_id = track.global_id
            len_feats = gid_2_lenfeats.get(track.global_id, -1)
            len_feats = ' ' if len_feats == 50 else len_feats 
            img = visualize_map(loc, img, cam_id, track_id, colors, len_feats, cur_frame)
    writer.write(img)
    return origin_img

def visualize_map(loc, img, cam_id, track_id, colors, len_feats, cur_frame):
    m = 2
    h, w, _ = img.shape
    loc[0], loc[1] = min(loc[0], w - 20), min(loc[1], h - 20)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f'{cam_id}/{track_id}/{len_feats}'
    txt_size = cv2.getTextSize(text, font, 0.4*m, 1*m)[0]
    color = (colors[track_id%80] * 255).astype(np.uint8).tolist()
    cv2.line(img, loc, loc, color, m)
    cv2.putText(img, text, (loc[0], loc[1] + txt_size[1]), font, 0.4*m, color, thickness=1*m)

    text = 'Frame : {}'.format(cur_frame)
    txt_size = cv2.getTextSize(text, font, 0.4*m, 1*m)[0]
    cv2.rectangle(img, (0, 0), (txt_size[0], int(1.5*txt_size[1])), (0,0,0), -1)
    cv2.putText(img, text, (0,txt_size[1]), font, 0.4*m, (255,255,255), thickness=1*m)

    return img