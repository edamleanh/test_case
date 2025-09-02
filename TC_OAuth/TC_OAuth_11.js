import { Selector } from 'testcafe';

fixture`Demo Login Test`
    .page`http://localhost:8000`;

const loginLink = Selector('a').withText('Log in');
const googleOAuthLink = Selector('a.github-icon');
const githubLoginInput = Selector('#login_field');
const githubPasswordInput = Selector('#password');
const githubSignInButton = Selector('input[type="submit"][name="commit"][value="Sign in"]');
const sitePasswordInput = Selector('#id_password');
const successMessage = Selector('span').withText('Hello, cotienxankle.');
const continueButton = Selector('input[type="submit"][value="Continue >"]');

test('User can log in with valid credentials', async t => {

    await t
        .click(loginLink)
        .click(googleOAuthLink)
        .click(githubLoginInput)
        .typeText(githubLoginInput, 'cotienxankle')
        .click(githubPasswordInput)
        .typeText(githubPasswordInput, 'Ducanh1305@!')
        .click(githubSignInButton)
        .click(sitePasswordInput)
        .typeText(sitePasswordInput, 'Ducanh12a1@!#')
        .click(continueButton)
        .click(continueButton)
        .expect(successMessage.exists).ok('Should show successful login message for cotienxankle');

});

