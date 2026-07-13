<?php
// Initialize database connection
$db_file = __DIR__ . '/../expo.db';
$is_new = !file_exists($db_file);

try {
    $db = new PDO('sqlite:' . $db_file);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    if ($is_new) {
        // Event registrations table
        $db->exec('CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            item_name TEXT,
            amount INTEGER
        )');
        
        // Stall bookings table
        $db->exec('CREATE TABLE IF NOT EXISTS stall_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            company_name TEXT,
            company_desc TEXT,
            package_name TEXT,
            amount INTEGER
        )');
        
        // Admins table
        $db->exec('CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )');
        
        // Default admin (password: "admin", hashed using password_hash)
        $hashed_pw = password_hash('admin', PASSWORD_DEFAULT);
        $stmt = $db->prepare('INSERT INTO admins (username, password) VALUES (?, ?)');
        $stmt->execute(['admin', $hashed_pw]);
    }
} catch (PDOException $e) {
    die(json_encode(['error' => 'Database connection failed: ' . $e->getMessage()]));
}

// Helper to check authentication
function check_auth() {
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }
    if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
        http_response_code(401);
        echo json_encode(['error' => 'Unauthorized']);
        exit;
    }
}
?>
