def _process_document_share(self, metadata):
    """Process document-specific sharing logic
    
    Args:
        metadata (dict): Document metadata containing sharing information
            Expected keys:
            - share_type: Type of sharing (public, private, specific_users)
            - users: List of user IDs to share with (for specific_users)
            - permissions: Dict of permission levels for each user
            - expiration: Optional expiration timestamp
    
    Returns:
        dict: Status of sharing operation with following keys:
            - success: Boolean indicating if share was successful
            - share_id: Unique identifier for this share
            - shared_with: List of users document was shared with
    """
    try:
        # Validate sharing metadata
        if not self._validate_share_metadata(metadata):
            raise ValueError("Invalid sharing metadata provided")

        # Set up sharing configuration
        share_config = {
            'document_id': self.document_id,
            'share_type': metadata.get('share_type', 'private'),
            'permissions': metadata.get('permissions', {}),
            'expiration': metadata.get('expiration')
        }

        # Process based on share type
        if share_config['share_type'] == 'public':
            share_id = self._create_public_share(share_config)
        elif share_config['share_type'] == 'specific_users':
            share_id = self._share_with_users(share_config, metadata.get('users', []))
        else:
            share_id = self._create_private_share(share_config)

        # Update document sharing status
        self._update_share_status(share_id, share_config)

        # Generate response
        return {
            'success': True,
            'share_id': share_id,
            'shared_with': metadata.get('users', []),
            'share_type': share_config['share_type'],
            'expiration': share_config['expiration']
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'share_id': None,
            'shared_with': []
        }