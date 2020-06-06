/** \file
* @brief Contains auxiliar functions for JSON object manipulation
******************************************************************************/

#include "auxiliar/jsonInterface.hpp"
#include <filesystem>
#include <string>

namespace fs = std::filesystem;

bool korali::isEmpty(knlohmann::json &js)
{
  bool empty = true;

  if (js.is_null()) return true;
  if (js.is_primitive()) return false;

  if (js.is_array())
  {
    for (size_t i = 0; i < js.size(); i++)
    {
      bool elEmpty = isEmpty(js[i]);
      if (elEmpty) js.erase(i--);
      empty = empty && elEmpty;
    }
  }

  if (js.is_object())
  {
    std::vector<std::string> erasedKeys;
    for (auto &el : js.items())
    {
      bool elEmpty = isEmpty(el.value());
      if (elEmpty == true) erasedKeys.push_back(el.key());
      empty = empty && elEmpty;
    }
    for (size_t i = 0; i < erasedKeys.size(); i++) js.erase(erasedKeys[i]);
  }

  return empty;
}

bool korali::isElemental(knlohmann::json &js)
{
  if (js.is_number()) return true;
  if (js.is_string()) return true;

  bool isArray = true;

  if (js.is_array())
  {
    for (size_t i = 0; i < js.size(); i++)
    {
      bool isElementArray = false;
      if (js[i].is_array()) isElementArray = isElemental(js[i]);
      if (js[i].is_number()) isElementArray = true;
      if (js[i].is_string()) isElementArray = true;
      isArray = isArray && isElementArray;
    }
  }
  else
    isArray = false;

  return isArray;
}

void korali::mergeJson(knlohmann::json &dest, const knlohmann::json &defaults)
{
  if (dest.is_object() == false)
  {
    fprintf(stderr, "Passed JSON A argument is not an object.\n");
    exit(-1);
  }
  if (defaults.is_object() == false)
  {
    fprintf(stderr, "Passed JSON B argument is not an object.\n");
    exit(-1);
  }

  for (auto &x : defaults.items())
  {
    auto k = x.key();
    if (dest.find(k) == dest.end()) // Key not found, copy now.
      dest[k] = defaults[k];
    else // Key found, check type.
      if (dest[k].is_object() && defaults[k].is_object())
      mergeJson(dest[k], defaults[k]); // Both are objects. Recurse within.
  }
}

bool korali::loadJsonFromFile(knlohmann::json &dst, const char *fileName)
{
  if (fs::exists(fileName))
  {
    // Getting path from filename
    fs::path filePath(fileName);

    // Getting actual location if file is symlink
    if (fs::is_symlink(fileName))
      filePath.replace_filename(fs::read_symlink(filePath));

    FILE *fid = fopen(filePath.c_str(), "r");
    if (fid != NULL)
    {
      fseek(fid, 0, SEEK_END);
      long fsize = ftell(fid);
      fseek(fid, 0, SEEK_SET); /* same as rewind(f); */

      char *string = (char *)malloc(fsize + 1);
      fread(string, 1, fsize, fid);
      fclose(fid);

      string[fsize] = '\0';

      dst = knlohmann::json::parse(string);

      free(string);
      return true;
    }
  }
  return false;
}

int korali::saveJsonToFile(const char *fileName, knlohmann::json &js)
{
  FILE *fid = fopen(fileName, "w");
  if (fid != NULL)
  {
    fprintf(fid, "%s", js.dump(1).c_str());
    fclose(fid);
  }
  else
  {
    return -1;
  }

  return 0;
}
