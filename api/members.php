<?php
require_once 'db.php';
check_auth();
header('Content-Type: application/json');

try {
    $stmt = $db->query('SELECT timestamp, name, email, phone, address, item_name, amount FROM members ORDER BY id DESC');
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode($rows);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Database error']);
}
?>
