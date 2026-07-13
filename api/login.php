<?php
require_once 'db.php';
session_start();
header('Content-Type: application/json');

$inputJSON = file_get_contents('php://input');
$input = json_decode($inputJSON, TRUE);

if (isset($input['username']) && isset($input['password'])) {
    $username = $input['username'];
    $password = $input['password'];
    
    $stmt = $db->prepare('SELECT id, password FROM admins WHERE username = ?');
    $stmt->execute([$username]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if ($row && password_verify($password, $row['password'])) {
        $_SESSION['admin_logged_in'] = true;
        echo json_encode(['status' => 'success']);
    } else {
        http_response_code(401);
        echo json_encode(['error' => 'Invalid credentials']);
    }
} else {
    http_response_code(400);
    echo json_encode(['error' => 'Missing username or password']);
}
?>
