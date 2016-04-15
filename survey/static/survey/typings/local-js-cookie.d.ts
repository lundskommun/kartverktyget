/*
 * Custom js-cookie typing.
 */

interface CookiesStatic {
    get(name: string): string;
    set(name: string, value: string);
}

declare var Cookies: CookiesStatic;