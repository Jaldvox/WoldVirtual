def process_sharing(self, metadata, resource_type='generic'):
        """
        Unified function to handle all sharing-related processing
        
        Args:
            metadata (dict): Metadata about the resource being shared
            resource_type (str): Type of resource ('image', 'video', or 'generic')
        
        Returns:
            bool: True if sharing process completed successfully, False otherwise
        """
        try:
            # Process based on resource type
            if resource_type == 'image':
                # Image-specific processing
                self._validate_image_format(metadata)
                self._optimize_image_for_sharing(metadata)
                
            elif resource_type == 'video':
                # Video-specific processing
                self._check_video_duration(metadata)
                self._ensure_video_compatibility(metadata)
                
            # Common sharing operations
            self._check_sharing_permissions(metadata)
            self._prepare_sharing_links(metadata)
            
            # Send notifications to relevant users
            notification_data = {
                'resource_type': resource_type,
                'shared_by': metadata.get('user_id'),
                'shared_with': metadata.get('recipients', []),
                'timestamp': datetime.now()
            }
            self._send_notifications(notification_data)
            
            # Update sharing statistics
            stats_update = {
                'share_count': 1,
                'resource_type': resource_type,
                'user_metrics': self._calculate_user_metrics(metadata)
            }
            self._update_stats(stats_update)
            
            return True
            
        except Exception as e:
            # Log any errors that occur during the process
            error_data = {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'metadata': metadata,
                'resource_type': resource_type
            }
            self._log_error(e, error_data)
            return False
