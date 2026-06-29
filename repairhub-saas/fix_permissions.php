<?php
// Hostinger Permission Fixer for BizHub AI
// This script recursively sets folders to 755 and files to 644
// to fix the EACCES build error.

function fixPermissions($dir) {
    $iterator = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS),
        RecursiveIteratorIterator::SELF_FIRST
    );

    foreach ($iterator as $item) {
        if ($item->isDir()) {
            chmod($item->getPathname(), 0755);
        } else {
            chmod($item->getPathname(), 0644);
        }
    }
}

$root = __DIR__;
fixPermissions($root);
echo "Permissions fixed! app/api/chat is now readable. You can delete this file and redeploy.";
?>
