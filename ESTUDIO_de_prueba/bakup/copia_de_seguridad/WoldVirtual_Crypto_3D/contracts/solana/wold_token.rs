use anchor_lang::prelude::*;
use anchor_spl::token::{self, Mint, Token, TokenAccount};
use anchor_spl::associated_token::AssociatedToken;

declare_id!("WoldToken1111111111111111111111111111111111111");

#[program]
pub mod wold_token {
    use super::*;

    pub fn initialize(
        ctx: Context<Initialize>,
        name: String,
        symbol: String,
        decimals: u8,
    ) -> Result<()> {
        let token_info = &mut ctx.accounts.token_info;
        token_info.authority = ctx.accounts.authority.key();
        token_info.name = name;
        token_info.symbol = symbol;
        token_info.decimals = decimals;
        token_info.total_supply = 0;
        Ok(())
    }

    pub fn mint(
        ctx: Context<Mint>,
        amount: u64,
    ) -> Result<()> {
        let token_info = &mut ctx.accounts.token_info;
        require!(
            ctx.accounts.authority.key() == token_info.authority,
            WoldTokenError::Unauthorized
        );

        token::mint_to(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                token::MintTo {
                    mint: ctx.accounts.mint.to_account_info(),
                    to: ctx.accounts.to.to_account_info(),
                    authority: ctx.accounts.authority.to_account_info(),
                },
            ),
            amount,
        )?;

        token_info.total_supply = token_info.total_supply.checked_add(amount)
            .ok_or(WoldTokenError::Overflow)?;

        Ok(())
    }

    pub fn burn(
        ctx: Context<Burn>,
        amount: u64,
    ) -> Result<()> {
        let token_info = &mut ctx.accounts.token_info;
        require!(
            ctx.accounts.authority.key() == token_info.authority,
            WoldTokenError::Unauthorized
        );

        token::burn(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                token::Burn {
                    mint: ctx.accounts.mint.to_account_info(),
                    from: ctx.accounts.from.to_account_info(),
                    authority: ctx.accounts.authority.to_account_info(),
                },
            ),
            amount,
        )?;

        token_info.total_supply = token_info.total_supply.checked_sub(amount)
            .ok_or(WoldTokenError::Underflow)?;

        Ok(())
    }

    pub fn transfer(
        ctx: Context<Transfer>,
        amount: u64,
    ) -> Result<()> {
        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                token::Transfer {
                    from: ctx.accounts.from.to_account_info(),
                    to: ctx.accounts.to.to_account_info(),
                    authority: ctx.accounts.authority.to_account_info(),
                },
            ),
            amount,
        )?;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = authority, space = TokenInfo::LEN)]
    pub token_info: Account<'info, TokenInfo>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Mint<'info> {
    #[account(mut)]
    pub token_info: Account<'info, TokenInfo>,
    #[account(mut)]
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub to: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct Burn<'info> {
    #[account(mut)]
    pub token_info: Account<'info, TokenInfo>,
    #[account(mut)]
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub from: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
}

#[derive(Accounts)]
pub struct Transfer<'info> {
    #[account(mut)]
    pub from: Account<'info, TokenAccount>,
    #[account(mut)]
    pub to: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
}

#[account]
pub struct TokenInfo {
    pub authority: Pubkey,
    pub name: String,
    pub symbol: String,
    pub decimals: u8,
    pub total_supply: u64,
}

impl TokenInfo {
    pub const LEN: usize = 8 + 32 + 32 + 4 + 1 + 8;
}

#[error_code]
pub enum WoldTokenError {
    #[msg("Unauthorized")]
    Unauthorized,
    #[msg("Overflow")]
    Overflow,
    #[msg("Underflow")]
    Underflow,
} 