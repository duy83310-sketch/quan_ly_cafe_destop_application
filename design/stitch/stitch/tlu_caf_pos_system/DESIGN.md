---
name: TLU Café POS System
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#5a403c'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#8e706b'
  outline-variant: '#e3beb8'
  surface-tint: '#b52619'
  primary: '#610000'
  on-primary: '#ffffff'
  primary-container: '#8b0000'
  on-primary-container: '#ff907f'
  inverse-primary: '#ffb4a8'
  secondary: '#934b00'
  on-secondary: '#ffffff'
  secondary-container: '#fea054'
  on-secondary-container: '#703800'
  tertiary: '#3b2a00'
  on-tertiary: '#ffffff'
  tertiary-container: '#573f00'
  on-tertiary-container: '#dfa600'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad4'
  primary-fixed-dim: '#ffb4a8'
  on-primary-fixed: '#410000'
  on-primary-fixed-variant: '#920703'
  secondary-fixed: '#ffdcc5'
  secondary-fixed-dim: '#ffb781'
  on-secondary-fixed: '#301400'
  on-secondary-fixed-variant: '#703800'
  tertiary-fixed: '#ffdfa0'
  tertiary-fixed-dim: '#fbbc00'
  on-tertiary-fixed: '#261a00'
  on-tertiary-fixed-variant: '#5c4300'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 44px
    fontWeight: '700'
    lineHeight: 52px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin-mobile: 16px
  margin-tablet: 24px
---

## Brand & Style

The design system is engineered for the fast-paced environment of high-volume food and beverage service. It balances the heritage of Thuyloi University with the modern requirements of a Point of Sale (POS) interface. The brand personality is **efficient, authoritative, and dependable.**

The chosen style is **Corporate Modern**, prioritizing utility and cognitive ease. It utilizes a refined structural grid to ensure that baristas and managers can navigate the interface with muscle memory. The aesthetic avoids unnecessary ornamentation, focusing instead on high-contrast touch targets and a clear visual hierarchy that reduces errors during peak hours. The emotional response should be one of "calm control"—even when the cafe is at its busiest.

## Colors

The color palette is rooted in a **Deep Burgundy (#8B0000)**, serving as the primary brand anchor and the color for critical actions (Submit Order, Pay). The **Warm Amber (#B5651D)** secondary color is used for navigational cues and category highlighting, evoking the warmth of coffee culture.

We employ a "Neutral-First" approach for the background to minimize eye strain. The interface uses **Soft Grays** for container strokes and **Clean Whites** for the primary workspace. High-contrast status colors (Green for "Completed", Amber for "Pending") are used sparingly to ensure they capture immediate attention without cluttering the visual field.

## Typography

This design system utilizes **Inter** exclusively to maximize legibility across varying screen brightness levels. The typographic scale is optimized for "at-a-glance" reading. 

- **Numerical Data:** For price points and order numbers, use `title-lg` with a semi-bold weight to ensure they stand out in a list.
- **Hierarchy:** Headlines use tighter letter-spacing to maintain a professional, compact appearance. 
- **Touch Targets:** Labels for buttons never drop below `label-lg` (14px) to ensure readability for users in motion.

## Layout & Spacing

The layout follows a **Fluid Grid** model with strict adherence to an 8px spacing system, ensuring all touch targets meet the minimum 44x44pt requirement for mobile accessibility. 

- **Mobile:** A 4-column layout with 16px side margins. Order items are displayed in a single-column vertical list for easy thumb-scrolling.
- **Tablet (POS Mode):** A 12-column layout. The screen is split into a 70/30 ratio: the left 70% features a responsive grid of product tiles, while the right 30% is a fixed "persistent receipt" sidebar.
- **Rhythm:** Use `md` (16px) for standard gutters between interactive cards and `xs` (8px) for internal padding within those cards.

## Elevation & Depth

To maintain a clean, professional aesthetic, this design system uses **Tonal Layers** combined with **Ambient Shadows**. 

Depth is used to signify interactivity:
- **Level 0 (Surface):** The main background using the neutral off-white.
- **Level 1 (Cards):** Primary containers for products and menu categories. These use a very soft, 10% opacity shadow with a 4px blur to lift them slightly from the background.
- **Level 2 (Modals/Active States):** Pop-overs for item modifications or payment processing. These use a more pronounced shadow (20% opacity, 12px blur) to focus the user's attention.
- **Interaction:** Avoid heavy bevels; instead, use a 1px inner stroke in a slightly darker neutral shade to define edges clearly under bright cafe lighting.

## Shapes

The shape language is **Rounded (0.5rem base)**. This soft geometry makes the interface feel approachable and modern while remaining efficient. 

- **Standard Buttons & Inputs:** Use the base `rounded` (8px) setting.
- **Category Chips:** Use `rounded-xl` (24px) to create a distinct visual pill shape that differentiates navigation from action buttons.
- **Product Tiles:** Use `rounded-lg` (16px) to give menu items a friendly, tactile appearance that invites tapping.

## Components

### Buttons
- **Primary Action:** Solid Deep Burgundy with white text. High-contrast and bold.
- **Secondary Action:** Ghost style (Burgundy border, transparent background).
- **Destructive:** Bright red text on a subtle light-red background (used for "Void Order").

### Product Tiles
- Large, touch-friendly containers with an image area and a footer for the price.
- **Active State:** When an item is selected, the tile should gain a 2px Burgundy border and a subtle amber tint.

### Input Fields
- Enclosed boxes with a 1px light gray border. 
- Labels should always be visible (top-aligned) to ensure context isn't lost during data entry.

### The "Order Bar" (Persistent Footer)
- A high-contrast bar at the bottom of the screen showing "Total" and a massive "Pay" button. This component is pinned to ensure the primary goal is always accessible.

### Selection Controls
- **Checkboxes & Radios:** Use large, 24px circles/squares to accommodate rapid selections for modifiers (e.g., extra sugar, oat milk).
- **Quantity Toggles:** Large "-" and "+" buttons flanking a bold number to minimize input errors.