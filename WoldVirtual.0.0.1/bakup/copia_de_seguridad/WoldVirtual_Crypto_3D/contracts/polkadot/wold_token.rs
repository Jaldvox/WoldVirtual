#![cfg_attr(not(feature = "std"), no_std)]

use ink_lang as ink;

#[ink::contract]
mod wold_token {
    use ink_storage::{
        collections::HashMap as StorageHashMap,
        traits::{PackedLayout, SpreadLayout},
    };

    #[ink(storage)]
    pub struct WoldToken {
        total_supply: Balance,
        balances: StorageHashMap<AccountId, Balance>,
        allowances: StorageHashMap<(AccountId, AccountId), Balance>,
        owner: AccountId,
        name: String,
        symbol: String,
        decimals: u8,
    }

    #[ink(event)]
    pub struct Transfer {
        #[ink(topic)]
        from: Option<AccountId>,
        #[ink(topic)]
        to: Option<AccountId>,
        value: Balance,
    }

    #[ink(event)]
    pub struct Approval {
        #[ink(topic)]
        owner: AccountId,
        #[ink(topic)]
        spender: AccountId,
        value: Balance,
    }

    #[derive(Debug, PartialEq, Eq, scale::Encode, scale::Decode)]
    #[cfg_attr(feature = "std", derive(scale_info::TypeInfo))]
    pub enum Error {
        InsufficientBalance,
        InsufficientAllowance,
        Unauthorized,
    }

    pub type Result<T> = core::result::Result<T, Error>;

    impl WoldToken {
        #[ink(constructor)]
        pub fn new(name: String, symbol: String, decimals: u8) -> Self {
            let owner = Self::env().caller();
            let total_supply = 1_000_000_000 * 10u128.pow(decimals as u32); // 1 billón de tokens

            let mut balances = StorageHashMap::new();
            balances.insert(owner, total_supply);

            Self {
                total_supply,
                balances,
                allowances: StorageHashMap::new(),
                owner,
                name,
                symbol,
                decimals,
            }
        }

        #[ink(message)]
        pub fn name(&self) -> String {
            self.name.clone()
        }

        #[ink(message)]
        pub fn symbol(&self) -> String {
            self.symbol.clone()
        }

        #[ink(message)]
        pub fn decimals(&self) -> u8 {
            self.decimals
        }

        #[ink(message)]
        pub fn total_supply(&self) -> Balance {
            self.total_supply
        }

        #[ink(message)]
        pub fn balance_of(&self, owner: AccountId) -> Balance {
            self.balances.get(&owner).copied().unwrap_or(0)
        }

        #[ink(message)]
        pub fn transfer(&mut self, to: AccountId, value: Balance) -> Result<()> {
            let from = self.env().caller();
            self.transfer_from_to(from, to, value)
        }

        #[ink(message)]
        pub fn approve(&mut self, spender: AccountId, value: Balance) -> Result<()> {
            let owner = self.env().caller();
            self.allowances.insert((owner, spender), value);
            self.env().emit_event(Approval {
                owner,
                spender,
                value,
            });
            Ok(())
        }

        #[ink(message)]
        pub fn transfer_from(
            &mut self,
            from: AccountId,
            to: AccountId,
            value: Balance,
        ) -> Result<()> {
            let caller = self.env().caller();
            let allowance = self.allowance(from, caller);
            if allowance < value {
                return Err(Error::InsufficientAllowance);
            }
            self.allowances.insert((from, caller), allowance - value);
            self.transfer_from_to(from, to, value)
        }

        #[ink(message)]
        pub fn allowance(&self, owner: AccountId, spender: AccountId) -> Balance {
            self.allowances.get(&(owner, spender)).copied().unwrap_or(0)
        }

        #[ink(message)]
        pub fn mint(&mut self, to: AccountId, value: Balance) -> Result<()> {
            let caller = self.env().caller();
            if caller != self.owner {
                return Err(Error::Unauthorized);
            }
            let balance = self.balance_of(to);
            self.balances.insert(to, balance + value);
            self.total_supply += value;
            self.env().emit_event(Transfer {
                from: None,
                to: Some(to),
                value,
            });
            Ok(())
        }

        #[ink(message)]
        pub fn burn(&mut self, from: AccountId, value: Balance) -> Result<()> {
            let caller = self.env().caller();
            if caller != self.owner {
                return Err(Error::Unauthorized);
            }
            let balance = self.balance_of(from);
            if balance < value {
                return Err(Error::InsufficientBalance);
            }
            self.balances.insert(from, balance - value);
            self.total_supply -= value;
            self.env().emit_event(Transfer {
                from: Some(from),
                to: None,
                value,
            });
            Ok(())
        }

        fn transfer_from_to(
            &mut self,
            from: AccountId,
            to: AccountId,
            value: Balance,
        ) -> Result<()> {
            let from_balance = self.balance_of(from);
            if from_balance < value {
                return Err(Error::InsufficientBalance);
            }
            self.balances.insert(from, from_balance - value);
            let to_balance = self.balance_of(to);
            self.balances.insert(to, to_balance + value);
            self.env().emit_event(Transfer {
                from: Some(from),
                to: Some(to),
                value,
            });
            Ok(())
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        use ink_lang as ink;

        #[ink::test]
        fn new_works() {
            let token = WoldToken::new(
                String::from("Wold Token"),
                String::from("WOLD"),
                18,
            );
            assert_eq!(token.name(), "Wold Token");
            assert_eq!(token.symbol(), "WOLD");
            assert_eq!(token.decimals(), 18);
            assert_eq!(token.total_supply(), 1_000_000_000 * 10u128.pow(18));
        }

        #[ink::test]
        fn transfer_works() {
            let mut token = WoldToken::new(
                String::from("Wold Token"),
                String::from("WOLD"),
                18,
            );
            let accounts = ink_env::test::default_accounts::<ink_env::DefaultEnvironment>();
            assert_eq!(token.balance_of(accounts.alice), 1_000_000_000 * 10u128.pow(18));
            assert_eq!(token.transfer(accounts.bob, 100), Ok(()));
            assert_eq!(token.balance_of(accounts.alice), 1_000_000_000 * 10u128.pow(18) - 100);
            assert_eq!(token.balance_of(accounts.bob), 100);
        }
    }
} 