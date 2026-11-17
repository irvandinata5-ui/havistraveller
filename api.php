<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$dataDir = __DIR__ . '/storage';
$uploadDir = __DIR__ . '/uploads';
if (!is_dir($dataDir)) @mkdir($dataDir, 0755, true);
if (!is_dir($uploadDir)) @mkdir($uploadDir, 0755, true);

$htFile = $dataDir . '/.htaccess';
if (!file_exists($htFile)) {
    @file_put_contents($htFile, "Order deny,allow\nDeny from all\n");
}

$dbFile = $dataDir . '/havist_db.json';
$action = isset($_GET['action']) ? $_GET['action'] : 'load';

if ($action === 'load') {
    if (file_exists($dbFile)) {
        readfile($dbFile);
    } else {
        echo json_encode(['_empty' => true]);
    }
    exit;
}

if ($action === 'save' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw = file_get_contents('php://input');
    $decoded = json_decode($raw, true);
    if (!is_array($decoded)) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'Invalid JSON']);
        exit;
    }
    $decoded['_updatedAt'] = gmdate('c');
    @file_put_contents($dbFile, json_encode($decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
    echo json_encode(['ok' => true, 'updatedAt' => $decoded['_updatedAt']]);
    exit;
}

if ($action === 'upload' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'Upload gagal']);
        exit;
    }
    $ext = strtolower(pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION));
    $allowed = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'pdf'];
    if (!in_array($ext, $allowed, true)) {
        http_response_code(400);
        echo json_encode(['ok' => false, 'error' => 'Format file tidak didukung']);
        exit;
    }
    $safeName = 'ht_' . date('Ymd_His') . '_' . substr(md5(uniqid('', true)), 0, 6) . '.' . $ext;
    $dest = $uploadDir . '/' . $safeName;
    if (move_uploaded_file($_FILES['file']['tmp_name'], $dest)) {
        echo json_encode(['ok' => true, 'url' => 'uploads/' . $safeName]);
    } else {
        http_response_code(500);
        echo json_encode(['ok' => false, 'error' => 'Gagal menyimpan file']);
    }
    exit;
}

echo json_encode(['ok' => false, 'error' => 'Unknown action']);
