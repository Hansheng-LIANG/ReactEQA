import trimesh
import numpy as np
import pickle


def visualize(scene_path, objects_path, unexcepts=["wall"]):
    # 1. 加载 GLB 场景
    scene = trimesh.load(scene_path)

    data = pickle.load(open(objects_path, "rb"))

    for obj in data['objects']:
        bbox = obj['bbox']
        name = obj['category_name']
        color = obj['color']

        if name in unexcepts:
            continue

        # 创建 Bounding Box
        bbox_min = np.array(bbox['min'])
        bbox_max = np.array(bbox['max'])
        bbox_center = np.array(bbox['center'])
        bbox_dimensions = np.array(bbox['dimensions'])

        # 创建 Bounding Box 可视化
        vertices = np.array([
        [bbox_min[0], bbox_min[1], bbox_min[2]],  # 0
        [bbox_max[0], bbox_min[1], bbox_min[2]],  # 1
        [bbox_max[0], bbox_max[1], bbox_min[2]],  # 2
        [bbox_min[0], bbox_max[1], bbox_min[2]],  # 3
        [bbox_min[0], bbox_min[1], bbox_max[2]],  # 4
        [bbox_max[0], bbox_min[1], bbox_max[2]],  # 5
        [bbox_max[0], bbox_max[1], bbox_max[2]],  # 6
        [bbox_min[0], bbox_max[1], bbox_max[2]]   # 7
        ])
        edges = np.array([
        [0, 1], [1, 2], [2, 3], [3, 0],  # 底面
        [4, 5], [5, 6], [6, 7], [7, 4],  # 顶面
        [0, 4], [1, 5], [2, 6], [3, 7]   # 侧面
        ])
        bbox_lines = []
        for edge in edges:
            # 每条边转换为圆柱（segment 是两点的坐标）
            line = trimesh.creation.cylinder(
                radius=0.01,  # 边线粗细
                segment=vertices[edge]  # 必须是 (2, 3) 的数组
            )
            bbox_lines.append(line)
        bbox_wireframe = trimesh.util.concatenate(bbox_lines)
        # bbox_lines.visual.face_colors = color + [100] # 半透明

        # 添加到场景
        scene.add_geometry(bbox_wireframe)

    scene.export('HkseAnWCgqk_bbox.ply')

if __name__ == "__main__":
    scene_path = "data/HM3D/00006-HkseAnWCgqk/HkseAnWCgqk.glb"
    objects_path = "HkseAnWCgqk_objects.pkl"
    visualize(scene_path, objects_path)