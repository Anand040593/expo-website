<?php
require_once 'db.php';
header('Content-Type: application/json');

$inputJSON = file_get_contents('php://input');
$data = json_decode($inputJSON, TRUE);

if (!$data) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit;
}

try {
    if (isset($data['is_stall']) && $data['is_stall'] === true) {
        $stmt = $db->prepare('INSERT INTO stall_bookings (name, email, phone, address, company_name, company_desc, package_name, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        $stmt->execute([
            $data['name'] ?? '',
            $data['email'] ?? '',
            $data['phone'] ?? '',
            $data['address'] ?? '',
            $data['company_name'] ?? '',
            $data['company_desc'] ?? '',
            $data['item_name'] ?? '',
            $data['amount'] ?? 0
        ]);
    } else {
        $stmt = $db->prepare('INSERT INTO members (name, email, phone, address, item_name, amount) VALUES (?, ?, ?, ?, ?, ?)');
        $stmt->execute([
            $data['name'] ?? '',
            $data['email'] ?? '',
            $data['phone'] ?? '',
            $data['address'] ?? '',
            $data['item_name'] ?? '',
            $data['amount'] ?? 0
        ]);
    }
    
    echo json_encode(['status' => 'success']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Database error: ' . $e->getMessage()]);
}
?>
