def record_resource_sharing_event(self, data):
    """
    Log the sharing activity for auditing purposes.
    
    Args:
        data (dict): Dictionary containing sharing activity details including:
            - user_id: ID of the user performing the share
            - resource_id: ID of the shared resource
            - recipient_ids: List of recipient user IDs
            - share_type: Type of sharing (view, edit, etc.)
            - timestamp: Time when sharing occurred
            - permissions: Specific permissions granted
    """
    try:
        # Format the timestamp
        timestamp = datetime.now().isoformat()
        
        # Create detailed log entry
        log_entry = {
            'event_type': 'resource_sharing',
            'user_id': data.get('user_id'),
            'resource_id': data.get('resource_id'),
            'recipients': data.get('recipient_ids', []),
            'share_type': data.get('share_type'),
            'permissions': data.get('permissions', {}),
            'ip_address': self._get_client_ip(),
            'timestamp': timestamp,
            'status': 'success'
        }
        
        # Add additional metadata
        log_entry['metadata'] = {
            'platform': self._get_platform_info(),
            'browser': self._get_browser_info(),
            'geo_location': self._get_geo_location()
        }
        
        # Write to multiple logging destinations
        self._write_to_database(log_entry)
        self._write_to_audit_file(log_entry)
        
        # Send notification if configured
        if self.notify_on_share:
            self._send_admin_notification(log_entry)
            
    except Exception as e:
        error_log = {
            'event_type': 'sharing_error',
            'error_message': str(e),
            'original_data': data,
            'timestamp': datetime.now().isoformat()
        }
        self._write_to_error_log(error_log)
        raise LoggingError(f"Failed to log sharing activity: {str(e)}")