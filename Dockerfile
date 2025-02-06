# Use the official Odoo 16 image
FROM odoo:16

# Set working directory to Odoo's root directory
WORKDIR /usr/lib/python3/dist-packages/odoo

# Copy your custom Odoo files (if any)
COPY addons/custom_module/ /mnt/extra-addons

# Set environment variables for database connection (from Railway)
ENV HOST=$DB_HOST
ENV USER=$DB_USER
ENV PASSWORD=$DB_PASSWORD

# Expose default Odoo web port
EXPOSE 8069

# Start Odoo with correct database connection
CMD ["odoo", "--db_host=$DB_HOST", "--db_user=$DB_USER", "--db_password=$DB_PASSWORD"]
