import { Selector } from 'testcafe';

fixture`Demo Login Test`
    .page`http://localhost:8000`;

const loginLink = Selector('a').withText('Log in');
const googleOAuthLink = Selector('a.github-icon');
const githubLoginInput = Selector('#login_field');
const githubPasswordInput = Selector('#password');
const githubSignInButton = Selector('input[type="submit"][name="commit"][value="Sign in"]');
const sitePasswordInput = Selector('#id_password');
const errorMessage = Selector('div.js-flash-alert').withText('Incorrect username or password.');

test('User can log in with valid credentials', async t => {

    await t
        .click(loginLink)
        .click(googleOAuthLink)
        .click(githubLoginInput)
        .typeText(githubLoginInput, 'cotienxankle')
        .click(githubPasswordInput)
        .typeText(githubPasswordInput, 'Ducanh1305@')
        .click(githubSignInButton)
        .expect(errorMessage.exists).ok('Should show error message for incorrect username or password');
});

