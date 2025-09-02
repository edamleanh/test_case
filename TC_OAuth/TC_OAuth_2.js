import { Selector } from 'testcafe';

fixture`Demo Login Test`
    .page`http://localhost:8000`;

const loginLink = Selector('a').withText('Log in');
const googleOAuthLink = Selector('a.google-icon');
const emailInput = Selector('input#identifierId');
const passwordInput = Selector('input[type="password"][name="Passwd"]');

test('User can log in with valid credentials', async t => {

    await t
        .click(loginLink)
        .click(googleOAuthLink)
        .click(emailInput)
        .typeText(emailInput, 'levoducanh8a1@gmail.com')
        .wait(1000000)
        .pressKey('enter')
        .click(passwordInput)
        .typeText(passwordInput, 'Ducanh12a1@')
        .pressKey('enter')
        .wait(10000); 

});

