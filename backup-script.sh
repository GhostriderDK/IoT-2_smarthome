#!/usr/bin/env sh

# Mapper
sourcedir="test"
zipname="backup.zip"
rclone_dest="azure:backup"


echo " **   Starting backup script ** "
echo " **   Testing connection to Azure... **"
rclone lsd "$rclone_dest"

echo " **   Zipping files"

# Delete zip if it already exists
rm "$zipname"
zip -r "$zipname" "$sourcedir"

rclone copy "$zipname" azure:backup
