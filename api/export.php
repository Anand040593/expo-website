<?php
require_once 'db.php';
check_auth();

$is_stalls = isset($_GET['type']) && $_GET['type'] === 'stalls';

header('Content-Type: text/csv');
if ($is_stalls) {
    header('Content-Disposition: attachment; filename="stall_bookings.csv"');
    $stmt = $db->query('SELECT timestamp, name, email, phone, address, company_name, company_desc, package_name, amount FROM stall_bookings ORDER BY id DESC');
} else {
    header('Content-Disposition: attachment; filename="event_registrations.csv"');
    $stmt = $db->query('SELECT timestamp, name, email, phone, address, item_name, amount FROM members ORDER BY id DESC');
}

$output = fopen('php://output', 'w');

if ($is_stalls) {
    fputcsv($output, ['Timestamp', 'Name', 'Email', 'Phone', 'Address', 'Company Name', 'Company Details', 'Package', 'Amount Paid (INR)']);
} else {
    fputcsv($output, ['Timestamp', 'Name', 'Email', 'Phone', 'Address', 'Item/Event', 'Amount Paid (INR)']);
}

while ($row = $stmt->fetch(PDO::FETCH_NUM)) {
    fputcsv($output, $row);
}
fclose($output);
?>
