/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext } from "react"
import { Box as RadixThemesBox, Button as RadixThemesButton, Flex as RadixThemesFlex, Text as RadixThemesText } from "@radix-ui/themes"
import { EventLoopContext, StateContexts } from "$/utils/context"
import { Event, isTrue } from "$/utils/state"
import NextHead from "next/head"
import { jsx } from "@emotion/react"



export function Button_de57d7598567ffea627d0e8097218639 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_click_122a95868c2c388798c97f48846aab73 = useCallback(((...args) => (addEvents([(Event("reflex___state____state.woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.select_network", ({ ["network"] : "Solana" }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{css:({ ["fontSize"] : "0.7em", ["width"] : "100%", ["padding"] : "0.3em 0.6em", ["background"] : "white", ["borderRadius"] : "0", ["&:hover"] : ({ ["background"] : "#f0f0f0" }) }),onClick:on_click_122a95868c2c388798c97f48846aab73},
"Solana"
,)
  )
}

export function Button_80b619a3dd338d23cf91420ce9552aab () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_click_5e6aa8f07210403fad60d9a6bf0f8f63 = useCallback(((...args) => (addEvents([(Event("reflex___state____state.woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.select_network", ({ ["network"] : "Avalanche" }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{css:({ ["fontSize"] : "0.7em", ["width"] : "100%", ["padding"] : "0.3em 0.6em", ["background"] : "white", ["borderRadius"] : "0", ["&:hover"] : ({ ["background"] : "#f0f0f0" }) }),onClick:on_click_5e6aa8f07210403fad60d9a6bf0f8f63},
"Avalanche"
,)
  )
}

export function Button_0bb24c738f4793d43e4292d05e47dd17 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_click_88bd28aec5a53ea0e412d35ebffe9947 = useCallback(((...args) => (addEvents([(Event("reflex___state____state.woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.select_network", ({ ["network"] : "Polygon" }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{css:({ ["fontSize"] : "0.7em", ["width"] : "100%", ["padding"] : "0.3em 0.6em", ["background"] : "white", ["borderRadius"] : "0", ["&:hover"] : ({ ["background"] : "#f0f0f0" }) }),onClick:on_click_88bd28aec5a53ea0e412d35ebffe9947},
"Polygon"
,)
  )
}

export function Fragment_ff7de9f06103ede21416a2a30716b501 () {
  
  const reflex___state____state__woldvirtual_reddepruebas___woldvirtual_reddepruebas____state = useContext(StateContexts.reflex___state____state__woldvirtual_reddepruebas___woldvirtual_reddepruebas____state)





  
  return (
    jsx(
Fragment,
{},
(reflex___state____state__woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.show_networks_menu ? (jsx(
Fragment,
{},
jsx(
RadixThemesBox,
{css:({ ["position"] : "absolute", ["top"] : "40px", ["right"] : "0", ["backgroundColor"] : "white", ["border"] : "1px solid #ddd", ["borderRadius"] : "6px", ["boxShadow"] : "0 2px 8px rgba(0,0,0,0.1)", ["width"] : "160px", ["zIndex"] : "1000", ["padding"] : "0.5em 0" })},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "start" }),direction:"column",gap:"0"},
jsx(Button_923336987cf6213863905bfae4c2818c,{},)
,jsx(Button_a56a7426319ba44d288f95e67355c64a,{},)
,jsx(Button_0bb24c738f4793d43e4292d05e47dd17,{},)
,jsx(Button_80b619a3dd338d23cf91420ce9552aab,{},)
,jsx(Button_6b62055ea6811ddf88ae5da61ed7e8f4,{},)
,jsx(Button_de57d7598567ffea627d0e8097218639,{},)
,),),)) : (jsx(Fragment,{},)
)),)
  )
}

export function Button_923336987cf6213863905bfae4c2818c () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_click_9b42efc2bcbcf261b8e030c2cc763c7b = useCallback(((...args) => (addEvents([(Event("reflex___state____state.woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.select_network", ({ ["network"] : "Binance Smart Chain" }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{css:({ ["fontSize"] : "0.7em", ["width"] : "100%", ["padding"] : "0.3em 0.6em", ["background"] : "white", ["borderRadius"] : "0", ["&:hover"] : ({ ["background"] : "#f0f0f0" }) }),onClick:on_click_9b42efc2bcbcf261b8e030c2cc763c7b},
"Binance Smart Chain"
,)
  )
}

export function Button_a56a7426319ba44d288f95e67355c64a () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_click_424851140e91d330912a69b19b4dc04a = useCallback(((...args) => (addEvents([(Event("reflex___state____state.woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.select_network", ({ ["network"] : "Ethereum" }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{css:({ ["fontSize"] : "0.7em", ["width"] : "100%", ["padding"] : "0.3em 0.6em", ["background"] : "white", ["borderRadius"] : "0", ["&:hover"] : ({ ["background"] : "#f0f0f0" }) }),onClick:on_click_424851140e91d330912a69b19b4dc04a},
"Ethereum"
,)
  )
}

export function Button_6dcb3c21c74bdbbf5a373c9ab2658e92 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  const reflex___state____state__woldvirtual_reddepruebas___woldvirtual_reddepruebas____state = useContext(StateContexts.reflex___state____state__woldvirtual_reddepruebas___woldvirtual_reddepruebas____state)


  const on_click_afb0fed9a0f324e81f9ba220bb619f6c = useCallback(((...args) => (addEvents([(Event("reflex___state____state.woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.toggle_networks_menu", ({  }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{css:({ ["background"] : "#343a40", ["color"] : "white", ["fontSize"] : "0.65em", ["padding"] : "0.3em 0.6em", ["borderRadius"] : "4px", ["cursor"] : "pointer" }),onClick:on_click_afb0fed9a0f324e81f9ba220bb619f6c},
reflex___state____state__woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.selected_network
,)
  )
}

export function Button_6b62055ea6811ddf88ae5da61ed7e8f4 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_click_5b16314370bdf6f89f530f7f0c1ca824 = useCallback(((...args) => (addEvents([(Event("reflex___state____state.woldvirtual_reddepruebas___woldvirtual_reddepruebas____state.select_network", ({ ["network"] : "Arbitrum" }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{css:({ ["fontSize"] : "0.7em", ["width"] : "100%", ["padding"] : "0.3em 0.6em", ["background"] : "white", ["borderRadius"] : "0", ["&:hover"] : ({ ["background"] : "#f0f0f0" }) }),onClick:on_click_5b16314370bdf6f89f530f7f0c1ca824},
"Arbitrum"
,)
  )
}

export default function Component() {
    




  return (
    jsx(
Fragment,
{},
jsx(
RadixThemesFlex,
{css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["width"] : "100vw", ["height"] : "100vh", ["background"] : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" })},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack",css:({ ["border"] : "1px solid #0000CD", ["borderRadius"] : "12px", ["overflow"] : "hidden", ["width"] : "96vw", ["height"] : "96vh", ["backgroundColor"] : "#3CB371" }),direction:"column",gap:"0"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["height"] : "50px", ["backgroundColor"] : "#FFD700", ["paddingInlineStart"] : "1em", ["paddingInlineEnd"] : "1em", ["alignItems"] : "center", ["position"] : "relative" }),direction:"row",gap:"3"},
jsx(
RadixThemesText,
{as:"p",css:({ ["fontSize"] : "1.1em", ["color"] : "black", ["fontWeight"] : "bold" })},
"World Virtual"
,),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},)
,jsx(
RadixThemesText,
{as:"p",css:({ ["fontSize"] : "0.8em", ["color"] : "black", ["marginInlineStart"] : "0.5em", ["marginInlineEnd"] : "0.5em" })},
"Mapa del proyecto."
,),jsx(
RadixThemesText,
{as:"p",css:({ ["fontSize"] : "0.8em", ["color"] : "black", ["marginInlineStart"] : "0.5em", ["marginInlineEnd"] : "0.5em" })},
"Libro blanco"
,),jsx(
RadixThemesText,
{as:"p",css:({ ["fontSize"] : "0.8em", ["color"] : "black", ["marginInlineStart"] : "0.5em", ["marginInlineEnd"] : "0.5em" })},
"C\u00f3digo abierto"
,),jsx(
RadixThemesBox,
{css:({ ["position"] : "relative" })},
jsx(Button_6dcb3c21c74bdbbf5a373c9ab2658e92,{},)
,jsx(Fragment_ff7de9f06103ede21416a2a30716b501,{},)
,),),jsx(
RadixThemesFlex,
{css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["width"] : "100%", ["height"] : "100%", ["backgroundColor"] : "#3CB371", ["padding"] : "1em" })},
jsx(
RadixThemesBox,
{css:({ ["backgroundColor"] : "white", ["borderRadius"] : "16px", ["boxShadow"] : "0 4px 15px rgba(0,0,0,0.1)", ["width"] : "90%", ["height"] : "90%", ["padding"] : "2em", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center" })},
jsx(
RadixThemesFlex,
{align:"center",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"4"},
jsx(
RadixThemesText,
{as:"p",css:({ ["fontWeight"] : "bold", ["fontSize"] : "1.5em", ["color"] : "#333" })},
"\u00c1rea de Contenido Principal"
,),jsx(
RadixThemesText,
{as:"p",css:({ ["color"] : "#666", ["textAlign"] : "center" })},
"Aqu\u00ed va el contenido principal de la aplicaci\u00f3n."
,),jsx(
RadixThemesText,
{as:"p",css:({ ["color"] : "#888", ["fontSize"] : "0.9em", ["textAlign"] : "center" })},
"El \u00e1rea se ajusta autom\u00e1ticamente al tama\u00f1o de la ventana."
,),),),),),),jsx(
NextHead,
{},
jsx(
"title",
{},
"WoldvirtualReddepruebas | Index"
,),jsx("meta",{content:"favicon.ico",property:"og:image"},)
,),)
  )
}
